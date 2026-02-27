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
from app.utils.logger import logger

router = APIRouter()


# ------------------------ Job Post Route ------------------------


@router.post("/create_job_post", status_code=status.HTTP_201_CREATED)
async def create_job_post(
    payload: JobPostingSchema,
    db: Session = Depends(get_db),
):
    """
    Create job and trigger background matching.
    """

    try:
        job = await create_job_post_service(payload, db)

        # Fire-and-forget matching
        asyncio.create_task(run_matching(job["id"]))

        return custom_response(
            success=True,
            message="Job created successfully. Matching started.",
            data=job,
            code=status.HTTP_201_CREATED,
        )

    except Exception as exc:
        logger.exception("Error creating job")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job",
        )


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
