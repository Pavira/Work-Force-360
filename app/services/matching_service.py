import asyncio
from sqlalchemy import func
from app.core.websocket import manager
from app.db.session import SessionLocal
from app.models.job_model import JobPostingModel
from app.models.worker_models import (
    WorkerRegistrationModel,
    WorkerSubCategoryModel,
)

# Configuration
RADIUS_METERS = 20000  # 20km
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds


def find_matching_workers(db, job):
    """
    Returns top nearby available workers for the job.
    """
    return (
        db.query(WorkerRegistrationModel)
        .join(
            WorkerSubCategoryModel,
            WorkerSubCategoryModel.worker_id == WorkerRegistrationModel.id,
        )
        .filter(
            WorkerRegistrationModel.is_active.is_(True),
            # WorkerRegistrationModel.is_online.is_(True),
            WorkerRegistrationModel.is_available.is_(True),
            WorkerSubCategoryModel.sub_category_skill_id == job.sub_category_id,
            func.ST_DWithin(
                WorkerRegistrationModel.location,
                job.location,
                RADIUS_METERS,
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


async def run_matching(job_id: int):
    """
    Main matching loop.
    Tries MAX_RETRIES times before stopping.
    """

    for attempt in range(MAX_RETRIES):

        # 🔹 Single DB session per iteration
        with SessionLocal() as db:

            job = db.query(JobPostingModel).filter(JobPostingModel.id == job_id).first()

            # Stop if job already assigned or cancelled
            if not job or job.status != "searching":
                return

            workers = find_matching_workers(db, job)

            # If no workers found → wait and retry
            if not workers:
                print(f"[Matching] Attempt {attempt+1}: No workers found.")
                await asyncio.sleep(RETRY_DELAY)
                continue

            print(f"[Matching] Attempt {attempt+1}: Found {len(workers)} workers.")

            # Send job to top 5 workers
            for worker in workers[:10]:
                await manager.send_job(
                    worker.id,
                    {
                        "job_id": str(job.id),
                        "wage": job.wage,
                        "message": "New Job Nearby",
                    },
                )

        # 🔹 Wait for worker acceptance
        await asyncio.sleep(RETRY_DELAY)

        # 🔹 Check again if job was accepted
        with SessionLocal() as db:
            updated_job = (
                db.query(JobPostingModel).filter(JobPostingModel.id == job_id).first()
            )

            if updated_job and updated_job.status != "searching":
                print("[Matching] Job accepted. Stopping retries.")
                return

    print("[Matching] Max retries reached. No worker accepted.")
