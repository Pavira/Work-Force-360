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
RETRY_DELAY = 5  # seconds
TOTAL_RETRY_TIME = 60  # 3 minutes
MAX_ATTEMPTS = TOTAL_RETRY_TIME // RETRY_DELAY  # 12 attempts over 3 minutes


def find_matching_workers(db, job):
    return (
        db.query(WorkerRegistrationModel)
        .join(
            WorkerSubCategoryModel,
            WorkerSubCategoryModel.worker_id == WorkerRegistrationModel.id,
        )
        .filter(
            WorkerRegistrationModel.is_active.is_(True),
            WorkerRegistrationModel.is_online.is_(False),
            WorkerRegistrationModel.is_available.is_(False),
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
    print(f"\n🚀 Starting matching for Job {job_id}\n")

    for attempt in range(MAX_ATTEMPTS):

        with SessionLocal() as db:

            job = db.query(JobPostingModel).filter(JobPostingModel.id == job_id).first()

            # Stop if job already accepted or cancelled
            if not job or job.status != "searching":
                print("🛑 Job no longer searching. Stopping matching.")
                return

            workers = find_matching_workers(db, job)
            print(f"\n🔎 Attempt {attempt+1}/{MAX_ATTEMPTS}")

            if workers:
                print(f"✅ Found {len(workers)} workers:")
                for worker in workers:
                    print(f"   - {worker.id} | {worker.name}")

            # Send Message to top 5 workers
            # print(f"[Matching] Attempt {attempt+1}: Sending to workers")

            # # Send to top 5 workers
            # for worker in workers[:5]:
            #     await manager.send_job(
            #         worker.id,
            #         {
            #             "job_id": str(job.id),
            #             "wage": job.wage,
            #             "message": "New Job Nearby",
            #         },
            #     )
            else:
                print(f"[Matching] Attempt {attempt+1}: No workers found")

        # Wait before next retry
        await asyncio.sleep(RETRY_DELAY)

    # 🔴 If we reach here → 3 minutes passed
    with SessionLocal() as db:
        job = db.query(JobPostingModel).filter(JobPostingModel.id == job_id).first()

        if job and job.status == "searching":
            job.status = "no_match"
            db.commit()

            print("[Matching] 3 minutes passed. No worker accepted.")
            return

            # Notify customer
            # await manager.notify_customer(
            #     job.customer_id,
            #     {
            #         "job_id": str(job.id),
            #         "message": "Sorry, no worker matched your request.",
            #     },
            # )

    print("[Matching] 3 minutes passed. No worker accepted.")
