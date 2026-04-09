import asyncio
from datetime import datetime
import traceback
from uuid import UUID

from fastapi import HTTPException, status
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.websocket import manager
from app.db.session import SessionLocal
from app.models.company_models import CompanyModel
from app.models.job_model import JobPostingModel
from app.models.worker_models import WorkerRegistrationModel
from app.schemas.job_schema import JobPostingSchema
from app.services.fcm_service import send_fcm_notification
from app.services.matching_service import run_matching
from app.utils.logger import logger


async def create_job_post_service(payload: JobPostingSchema, db: Session) -> dict:
    try:
        location = from_shape(
            Point(payload.longitude, payload.latitude),  # lng, lat order
            srid=4326,
        )

        job = JobPostingModel(
            skill_category_id=payload.skillCategoryId,
            sub_category_id=payload.subCategoryId,
            industry_type_id=payload.industryTypeId,
            tier=payload.tier,
            description=payload.description,
            location=location,
            work_address=payload.workAddress,
            nearby_landmark=payload.nearbyLandmark,
            scheduled_start_datetime=payload.scheduledStartDateTime,
            scheduled_end_datetime=payload.scheduledEndDateTime,
            scheduled_duration=payload.scheduledDuration,
            duration_type=payload.durationType,
            shift=payload.shift,
            workers=payload.workers,
            experience_required=payload.experienceRequired,
            wage=payload.wage,
            expected_total=payload.expectedTotal,
            name=payload.name,
            country_code=payload.countryCode,
            phone_number=payload.phoneNumber,
            email=payload.email,
            language_preference=payload.languagePreference,
            tool_provided=payload.toolProvided,
            tool_details=payload.toolDetails,
            special_instructions=payload.specialInstructions,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Start event-driven matching only after the job is persisted
        asyncio.create_task(run_matching(job.id))

        return {
            "id": job.id,
        }

    except HTTPException:
        raise
    except Exception as e:
        print("create_job_post_service DB ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating job post",
        )


# ------------------------END Job Post Service ------------------------


# ------------------------GET All Job Post Service ------------------------
def get_all_job_posts_service(db: Session) -> list[JobPostingModel]:
    try:
        jobs = db.query(JobPostingModel).all()

        result = []
        for job in jobs:
            job_dict = {
                c.name: getattr(job, c.name)
                for c in job.__table__.columns
                if c.name != "location"  # exclude geography field
            }
            result.append(job_dict)

        return result

    except Exception as e:
        print("get_all_job_posts_service DB ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving job posts",
        )


# ------------------------END GET All Job Post Service ------------------------


# ------------------------GET Job Post By ID Service ------------------------
def get_job_post_by_id_service(job_id: str, db: Session) -> dict:
    try:
        try:
            parsed_job_id = UUID(job_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid job_id format",
            )

        job_post = (
            db.query(JobPostingModel)
            .filter(
                JobPostingModel.id == parsed_job_id,
                JobPostingModel.is_active == True,  # noqa: E712
            )
            .first()
        )
        if not job_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found"
            )

        point = to_shape(job_post.location) if job_post.location else None
        return {
            "id": str(job_post.id),
            "skillCategoryId": str(job_post.skill_category_id),
            "subCategoryId": (
                str(job_post.sub_category_id) if job_post.sub_category_id else None
            ),
            "industryTypeId": (
                str(job_post.industry_type_id) if job_post.industry_type_id else None
            ),
            "tier": job_post.tier,
            "description": job_post.description,
            "latitude": point.y if point else None,
            "longitude": point.x if point else None,
            "workAddress": job_post.work_address,
            "nearbyLandmark": job_post.nearby_landmark,
            "scheduledStartDateTime": job_post.scheduled_start_datetime,
            "scheduledEndDateTime": job_post.scheduled_end_datetime,
            "scheduledDuration": job_post.scheduled_duration,
            "durationType": job_post.duration_type,
            "shift": job_post.shift,
            "workers": job_post.workers,
            "experienceRequired": job_post.experience_required,
            "wage": job_post.wage,
            "expectedTotal": job_post.expected_total,
            "name": job_post.name,
            "countryCode": job_post.country_code,
            "phoneNumber": job_post.phone_number,
            "email": job_post.email,
            "languagePreference": job_post.language_preference,
            "toolProvided": job_post.tool_provided,
            "toolDetails": job_post.tool_details,
            "specialInstructions": job_post.special_instructions,
            "status": job_post.status,
            "postedAt": job_post.posted_at,
            "assignedAt": job_post.assigned_at,
            "startedAt": job_post.started_at,
            "completedAt": job_post.completed_at,
            "cancelledAt": job_post.cancelled_at,
            "createdAt": job_post.created_at,
            "updatedAt": job_post.updated_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("get_job_post_by_id_service DB ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving job post",
        )


# ------------------------END GET Job Post By ID Service ------------------------


# ------------------------Accept Job Service ------------------------
async def accept_job_service(job_id: UUID, worker_id: UUID, db: Session) -> dict:
    try:
        job = (
            db.query(JobPostingModel)
            .filter(
                JobPostingModel.id == job_id,
                JobPostingModel.status == "searching",
            )
            .first()
        )

        if not job:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job already taken",
            )

        worker = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.id == worker_id)
            .first()
        )
        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found",
            )

        updated = (
            db.query(JobPostingModel)
            .filter(
                JobPostingModel.id == job_id,
                JobPostingModel.status == "searching",
            )
            .update(
                {
                    "status": "assigned",
                    "assigned_worker_id": worker_id,
                    "assigned_at": func.now(),
                }
            )
        )

        if updated == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job already taken",
            )

        worker.is_available = False

        payload = {
            "type": "WORKER_ASSIGNED",
            "job_id": str(job_id),
            "worker_id": str(worker_id),
            "worker_name": worker.name,
            "status": "assigned",
        }

        db.flush()

        company_id = getattr(job, "company_id", None)
        if company_id:
            try:
                await manager.send_to_user(
                    "companies",
                    company_id,
                    payload,
                )
            except Exception:
                logger.exception(
                    "Failed to send company websocket notification for job_id=%s company_id=%s",
                    job_id,
                    company_id,
                )

            company = (
                db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
            )
            company_fcm_token = getattr(company, "fcm_token", None) if company else None

            if company_fcm_token:
                try:
                    await send_fcm_notification(
                        company_fcm_token,
                        payload,
                        title="Worker Assigned ✅",
                        body="A worker has accepted your job",
                    )
                except Exception:
                    logger.exception(
                        "Failed to send company FCM notification for job_id=%s company_id=%s",
                        job_id,
                        company_id,
                    )
        else:
            logger.warning(
                "No company_id found on job_id=%s, skipped company notifications",
                job_id,
            )

        return {"message": "Job Assigned"}
    except HTTPException:
        raise
    except Exception as e:
        print("accept_job_service DB ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error accepting job",
        )


# ------------------------END Accept Job Service ------------------------
