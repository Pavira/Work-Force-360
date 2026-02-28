# app/services/matching_service.py

import asyncio
from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.matching_config import (
    INITIAL_RADIUS_METERS,
    MAX_ATTEMPTS,
    MAX_RADIUS_METERS,
    RADIUS_INCREMENT_METERS,
    RETRY_DELAY_SECONDS,
)
from app.core.websocket import manager
from app.db.session import SessionLocal
from app.models.job_model import JobPostingModel
from app.models.worker_models import WorkerRegistrationModel, WorkerSubCategoryModel
from app.utils.logger import logger


def calculate_radius(attempt: int) -> int:
    """
    Dynamically increases radius per attempt until MAX_RADIUS_METERS is reached.
    """
    radius = INITIAL_RADIUS_METERS + (attempt * RADIUS_INCREMENT_METERS)
    return min(radius, MAX_RADIUS_METERS)


def find_matching_workers(
    db: Session,
    job: JobPostingModel,
    radius: int,
) -> List[WorkerRegistrationModel]:
    """
    Fetch nearest matching workers based on:
    - Active
    - Online
    - Available
    - Matching subcategory
    - Within radius (PostGIS ST_DWithin)
    """

    try:
        workers = (
            db.query(WorkerRegistrationModel)
            .join(
                WorkerSubCategoryModel,
                WorkerSubCategoryModel.worker_id == WorkerRegistrationModel.id,
            )
            .filter(
                WorkerRegistrationModel.is_active.is_(True),
                WorkerRegistrationModel.is_online.is_(True),
                WorkerRegistrationModel.is_available.is_(True),
                WorkerSubCategoryModel.sub_category_skill_id == job.sub_category_id,
                func.ST_DWithin(
                    WorkerRegistrationModel.location,
                    job.location,
                    radius,
                ),
            )
            .order_by(
                func.ST_Distance(
                    WorkerRegistrationModel.location,
                    job.location,
                )
            )
            .limit(10)
            .all()
        )

        return workers

    except SQLAlchemyError as db_error:
        logger.error("Database error during worker matching: %s", db_error)
        raise

    except Exception:
        logger.exception("Unexpected error in find_matching_workers")
        raise


async def run_matching(job_id: UUID) -> None:
    """
    Background matching engine.

    Flow:
    - Retry up to MAX_ATTEMPTS
    - Expand radius each attempt
    - Stop if job status changes
    - If timeout reached, mark as no_match and notify company websocket
    """

    logger.info("Matching started for Job: %s", job_id)

    try:
        for attempt in range(MAX_ATTEMPTS):
            radius = calculate_radius(attempt)

            try:
                with SessionLocal() as db:
                    job = (
                        db.query(JobPostingModel)
                        .filter(JobPostingModel.id == job_id)
                        .first()
                    )

                    if not job:
                        logger.warning("Job %s not found. Stopping matching.", job_id)
                        return

                    if job.status != "searching":
                        logger.info(
                            "Job %s status changed to %s. Stopping matching.",
                            job_id,
                            job.status,
                        )
                        return

                    workers = find_matching_workers(db, job, radius)

                    logger.info(
                        "Attempt %s/%s | Radius: %sm | Workers Found: %s",
                        attempt + 1,
                        MAX_ATTEMPTS,
                        radius,
                        len(workers),
                    )

                    if workers:
                        matched_worker = workers[0]

                        job.status = "Assigned"
                        job.assigned_worker_id = matched_worker.id
                        job.assigned_at = func.now()
                        matched_worker.is_available = False

                        try:
                            db.commit()
                        except SQLAlchemyError as commit_error:
                            db.rollback()
                            logger.error(
                                "Failed to assign worker for job %s: %s",
                                job_id,
                                commit_error,
                            )
                            continue

                        await manager.send_to_user(
                            "workers",
                            matched_worker.id,
                            {
                                "type": "JOB_ASSIGNED",
                                "job_id": job.id,
                                "work_address": job.work_address,
                                "scheduled_duration": job.scheduled_duration,
                                "duration_type": job.duration_type,
                                "wage": job.wage,
                                "workers_required": job.workers,
                                "phone_number": job.phone_number,
                                "status": "Assigned",
                            },
                        )

                        company_message = {
                            "type": "WORKER_MATCHED",
                            "job_id": job.id,
                            "worker_id": matched_worker.id,
                            "worker_name": matched_worker.name,
                            "status": "Assigned",
                        }
                        company_id = getattr(job, "company_id", None)
                        if company_id:
                            await manager.send_to_user(
                                "companies",
                                company_id,
                                company_message,
                            )
                        # else:
                        #     # Fallback when job has no company_id relation.
                        #     await manager.broadcast("companies", company_message)

                        logger.info(
                            "Job %s assigned to worker %s",
                            job_id,
                            matched_worker.id,
                        )
                        return

            except SQLAlchemyError as db_error:
                logger.error(
                    "Database error during attempt %s for job %s: %s",
                    attempt + 1,
                    job_id,
                    db_error,
                )
            except Exception:
                logger.exception(
                    "Unexpected error during matching attempt %s",
                    attempt + 1,
                )

            await asyncio.sleep(RETRY_DELAY_SECONDS)

        with SessionLocal() as db:
            job = db.query(JobPostingModel).filter(JobPostingModel.id == job_id).first()

            if job and job.status == "searching":
                job.status = "no_match"

                try:
                    db.commit()
                    logger.info("Job %s marked as no_match after timeout.", job_id)

                    timeout_message = {
                        "type": "MATCH_TIMEOUT",
                        "job_id": job_id,
                        "status": "NoWorkerMatch",
                    }
                    company_id = getattr(job, "company_id", None)
                    if company_id:
                        await manager.send_to_user(
                            "companies",
                            company_id,
                            timeout_message,
                        )
                    # else:
                    #     # Fallback when job has no company_id relation.
                    #     await manager.broadcast("companies", timeout_message)
                except SQLAlchemyError as commit_error:
                    db.rollback()
                    logger.error(
                        "Failed to update job %s to no_match: %s",
                        job_id,
                        commit_error,
                    )

    except Exception as fatal_error:
        logger.exception(
            "Critical failure in run_matching for job %s: %s",
            job_id,
            fatal_error,
        )
