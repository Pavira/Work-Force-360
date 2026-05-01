from fastapi import APIRouter, Depends, HTTPException, Query, Request, logger, status
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.job_schema import JobPostingSchema
from app.services.admin_panel_job_service import (
    admin_create_job_post_service,
    assign_job_to_worker_service,
    get_all_assigned_jobs_service,
    get_all_cancelled_jobs_service,
    get_all_completed_jobs_service,
    get_all_in_progress_jobs_service,
    get_all_nearest_workers_service,
    get_all_no_worker_match_jobs_service,
    get_all_searching_jobs_service,
    get_job_details_by_id_service,
)
from app.utils.response import custom_response

router = APIRouter()


@router.get(
    "/searching",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_searching_jobs(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    job_details = get_all_searching_jobs_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Searching job details and counts fetched successfully",
        data=job_details,
        code=status.HTTP_200_OK,
    )


@router.get(
    "/assigned",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_assigned_jobs(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    job_details = get_all_assigned_jobs_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Assigned job details and counts fetched successfully",
        data=job_details,
        code=status.HTTP_200_OK,
    )


@router.get(
    "/in_progress",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_in_progress_jobs(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    job_details = get_all_in_progress_jobs_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="In progress job details and counts fetched successfully",
        data=job_details,
        code=status.HTTP_200_OK,
    )


@router.get(
    "/completed",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_completed_jobs(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    job_details = get_all_completed_jobs_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Completed job details and counts fetched successfully",
        data=job_details,
        code=status.HTTP_200_OK,
    )


@router.get(
    "/cancelled",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_cancelled_jobs(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    job_details = get_all_cancelled_jobs_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Cancelled job details and counts fetched successfully",
        data=job_details,
        code=status.HTTP_200_OK,
    )


@router.get(
    "/no_worker_match",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_no_worker_match_jobs(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    job_details = get_all_no_worker_match_jobs_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="No worker match job details and counts fetched successfully",
        data=job_details,
        code=status.HTTP_200_OK,
    )


@router.get(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_job_details_by_id(
    request: Request,
    job_id: str,
    db: Session = Depends(get_db),
):
    job = get_job_details_by_id_service(db=db, job_id=job_id)

    return custom_response(
        success=True,
        message="Job details fetched successfully",
        data=job,
        code=status.HTTP_200_OK,
    )


@router.get(
    "/{job_id}/nearest_workers",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_nearest_workers(
    request: Request,
    job_id: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    workers = get_all_nearest_workers_service(
        db=db,
        job_id=job_id,
        limit=limit,
    )

    return custom_response(
        success=True,
        message="Nearest workers fetched successfully",
        data=workers,
        code=status.HTTP_200_OK,
    )


# ------------------------Assign Job to Worker Service----------------------- #
@router.post(
    "/{job_id}/assign/{worker_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
def assign_job_to_worker(
    request: Request,
    job_id: str,
    worker_id: str,
    db: Session = Depends(get_db),
):
    assign_job_to_worker_service(
        db=db,
        job_id=job_id,
        worker_id=worker_id,
    )

    return custom_response(
        success=True,
        message="Job assigned to worker successfully",
        code=status.HTTP_200_OK,
    )


# ------------------------Create New Job Service by Admin----------------------- #
@router.post("/create_job_post", status_code=status.HTTP_201_CREATED)
async def create_job_post(
    payload: JobPostingSchema,
    db: Session = Depends(get_db),
):
    """
    Create job and trigger background matching.
    """

    try:
        job = await admin_create_job_post_service(payload, db)

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
