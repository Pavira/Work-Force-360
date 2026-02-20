import asyncio
import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.firebase_auth import get_current_user
from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.job_schema import JobPostingSchema
from app.services.job_service import (
    accept_job_service,
    create_job_post_service,
    get_all_job_posts_service,
    get_job_post_by_id_service,
)
from app.services.matching_service import run_matching
from app.utils.response import custom_response


router = APIRouter()


# ------------------------ Job Post Route ------------------------


async def start_matching(job_id: UUID):
    try:
        print("🚀 Matching task started for:", job_id)

        await asyncio.sleep(0.1)

        print("⏳ Calling run_matching")

        await run_matching(job_id)

        print("✅ Matching finished")

    except Exception as e:
        print("❌ Matching crashed:", e)
        import traceback

        traceback.print_exc()


@router.post("/create_job_post", status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_job_post(
    request: Request,
    payload: JobPostingSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new job post.
    """
    try:
        job = await create_job_post_service(payload=payload, db=db)

        # 🔥 Start matching in background (non-blocking)
        task = asyncio.create_task(start_matching(job["id"]))
        print("Task object:", task)

        return custom_response(
            success=True,
            message="Job post created successfully",
            data=job,
            code=status.HTTP_201_CREATED,
        )

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise


# ------------------------END Job Post Route ------------------------


# ------------------------GET All Job Post Route ------------------------
@router.get("/get_all_job_posts", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_all_job_posts(request: Request, db: Session = Depends(get_db)):
    """
    Get all job posts.
    """

    job = get_all_job_posts_service(db=db)

    return custom_response(
        success=True,
        message="All job posts retrieved successfully",
        data=job,
        code=status.HTTP_200_OK,
    )


# ------------------------END GET All Job Post Route ------------------------


# ------------------------GET Job Post By ID Route ------------------------
@router.get("/get_job_post/{job_id}", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_job_post_by_id(request: Request, job_id: str, db: Session = Depends(get_db)):
    """
    Get a job post by ID.
    """

    job = get_job_post_by_id_service(job_id=job_id, db=db)

    return custom_response(
        success=True,
        message="Job post retrieved successfully",
        data=job,
        code=status.HTTP_200_OK,
    )


# ------------------------END GET Job Post By ID Route ------------------------


#
@router.post("/jobs/{job_id}/accept")
@limiter.limit("30/minute")
def accept_job(
    request: Request,
    job_id: UUID,
    worker_id: UUID,
    db: Session = Depends(get_db),
):
    result = accept_job_service(job_id=job_id, worker_id=worker_id, db=db)
    return custom_response(
        success=True,
        message="Job assigned successfully",
        data=result,
        code=status.HTTP_200_OK,
    )
