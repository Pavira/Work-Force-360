import logging
from uuid import UUID

from fastapi import HTTPException, status
from geoalchemy2.shape import to_shape
from sqlalchemy import String, func, or_
from sqlalchemy.orm import Session

from app.models.job_model import JobPostingModel

VALID_SEARCH_TYPES = {"contact_name", "phone", "company_id", "worker_id"}
JOB_STATUSES = [
    "searching",
    "assigned",
    "in_progress",
    "completed",
    "cancelled",
    "no_worker_match",
]
logger = logging.getLogger(__name__)


def _build_job_status_query(db: Session, target_status: str):
    return db.query(
        JobPostingModel.id,
        JobPostingModel.company_id,
        JobPostingModel.assigned_worker_id,
        JobPostingModel.name,
        JobPostingModel.phone_number,
        JobPostingModel.work_address,
        JobPostingModel.scheduled_start_datetime,
        JobPostingModel.status,
    ).filter(
        JobPostingModel.status == target_status,
        JobPostingModel.is_active.is_(True),
    )


def _apply_search_filters(query, search_term: str | None, search_type: str | None):
    if search_term is None or not search_term.strip():
        return query

    normalized_term = search_term.strip()

    if search_type not in VALID_SEARCH_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid search_type. Allowed values: "
                "contact_name, phone, company_id, worker_id"
            ),
        )

    term = f"%{normalized_term}%"
    if search_type == "contact_name":
        return query.filter(JobPostingModel.name.ilike(term))
    if search_type == "phone":
        return query.filter(
            or_(
                JobPostingModel.phone_number.ilike(term),
                JobPostingModel.country_code.ilike(term),
            )
        )
    if search_type == "company_id":
        return query.filter(func.cast(JobPostingModel.company_id, String).ilike(term))
    return query.filter(func.cast(JobPostingModel.assigned_worker_id, String).ilike(term))


def _safe_parse_cursor(cursor: str | None) -> UUID | None:
    if cursor is None:
        return None

    normalized = cursor.strip()
    if not normalized:
        return None

    try:
        return UUID(normalized)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cursor format. Expected UUID string.",
        ) from exc


def _get_status_counts(db: Session) -> dict:
    rows = (
        db.query(JobPostingModel.status, func.count(JobPostingModel.id))
        .filter(
            JobPostingModel.is_active.is_(True),
            JobPostingModel.status.in_(JOB_STATUSES),
        )
        .group_by(JobPostingModel.status)
        .all()
    )
    status_count_map = {status_name: count for status_name, count in rows}
    counts = {
        "searching_count": status_count_map.get("searching", 0),
        "assigned_count": status_count_map.get("assigned", 0),
        "in_progress_count": status_count_map.get("in_progress", 0),
        "completed_count": status_count_map.get("completed", 0),
        "cancelled_count": status_count_map.get("cancelled", 0),
        "no_worker_match_count": status_count_map.get("no_worker_match", 0),
    }
    counts["total_count"] = sum(counts.values())
    return counts


def _paginate_job_query(query, page: int, page_size: int, cursor: str | None):
    ordered_query = query.order_by(JobPostingModel.id.asc())
    parsed_cursor = _safe_parse_cursor(cursor)

    if parsed_cursor is not None:
        rows = ordered_query.filter(JobPostingModel.id > parsed_cursor).limit(page_size).all()
        next_cursor = str(rows[-1].id) if len(rows) == page_size else None
        prev_cursor = str(rows[0].id) if rows else None
        resolved_page = 1
        return rows, resolved_page, next_cursor, prev_cursor

    offset = (page - 1) * page_size
    rows = ordered_query.offset(offset).limit(page_size).all()
    return rows, page, None, None


def _serialize_job_rows(rows) -> list[dict]:
    items = []
    for row in rows:
        items.append(
            {
                "id": str(row.id),
                "company_id": str(row.company_id) if row.company_id else None,
                "assigned_worker_id": (
                    str(row.assigned_worker_id) if row.assigned_worker_id else None
                ),
                "name": row.name,
                "phone_number": row.phone_number,
                "work_address": row.work_address,
                "scheduled_start_datetime": row.scheduled_start_datetime,
                "status": row.status,
            }
        )
    return items


def _build_job_total_count_query(db: Session, target_status: str):
    return db.query(func.count(JobPostingModel.id)).filter(
        JobPostingModel.status == target_status,
        JobPostingModel.is_active.is_(True),
    )


def _apply_search_filters_to_count_query(
    query,
    search_term: str | None,
    search_type: str | None,
):
    if search_term is None or not search_term.strip():
        return query

    normalized_term = search_term.strip()
    term = f"%{normalized_term}%"

    if search_type == "contact_name":
        return query.filter(JobPostingModel.name.ilike(term))
    if search_type == "phone":
        return query.filter(
            or_(
                JobPostingModel.phone_number.ilike(term),
                JobPostingModel.country_code.ilike(term),
            )
        )
    if search_type == "company_id":
        return query.filter(func.cast(JobPostingModel.company_id, String).ilike(term))
    if search_type == "worker_id":
        return query.filter(func.cast(JobPostingModel.assigned_worker_id, String).ilike(term))
    return query


def _get_jobs_by_status_service(
    db: Session,
    target_status: str,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="page must be greater than or equal to 1",
        )
    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="page_size must be greater than or equal to 1",
        )
    if page_size > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="page_size must be less than or equal to 200",
        )

    query = _build_job_status_query(db=db, target_status=target_status)
    query = _apply_search_filters(
        query=query,
        search_term=search_term,
        search_type=search_type,
    )

    total_count_query = _build_job_total_count_query(db=db, target_status=target_status)
    total_count_query = _apply_search_filters_to_count_query(
        query=total_count_query,
        search_term=search_term,
        search_type=search_type,
    )
    total_count = total_count_query.scalar() or 0

    rows, resolved_page, next_cursor, prev_cursor = _paginate_job_query(
        query=query,
        page=page,
        page_size=page_size,
        cursor=cursor,
    )
    items = _serialize_job_rows(rows)

    return {
        "items": items,
        "filtered_total_count": total_count,
        "page": resolved_page,
        "page_size": page_size,
        "next_cursor": next_cursor,
        "prev_cursor": prev_cursor,
        **_get_status_counts(db=db),
    }


def get_all_searching_jobs_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_jobs_by_status_service(
            db=db,
            target_status="searching",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching searching job details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching searching job details",
        )


def get_all_assigned_jobs_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_jobs_by_status_service(
            db=db,
            target_status="assigned",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching assigned job details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching assigned job details",
        )


def get_all_in_progress_jobs_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_jobs_by_status_service(
            db=db,
            target_status="in_progress",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching in progress job details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching in progress job details",
        )


def get_all_completed_jobs_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_jobs_by_status_service(
            db=db,
            target_status="completed",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching completed job details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching completed job details",
        )


def get_all_cancelled_jobs_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_jobs_by_status_service(
            db=db,
            target_status="cancelled",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching cancelled job details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching cancelled job details",
        )


def get_all_no_worker_match_jobs_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_jobs_by_status_service(
            db=db,
            target_status="no_worker_match",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching no worker match job details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching no worker match job details",
        )


def get_job_details_by_id_service(db: Session, job_id: str) -> dict:
    try:
        try:
            parsed_job_id = UUID(job_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid job_id format. Expected UUID string.",
            ) from exc

        job_post = (
            db.query(JobPostingModel)
            .filter(
                JobPostingModel.id == parsed_job_id,
                JobPostingModel.is_active.is_(True),
            )
            .first()
        )
        if not job_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job post not found",
            )

        point = to_shape(job_post.location) if job_post.location else None
        return {
            "id": str(job_post.id),
            "company_id": str(job_post.company_id) if job_post.company_id else None,
            "skill_category_id": (
                str(job_post.skill_category_id) if job_post.skill_category_id else None
            ),
            "sub_category_id": (
                str(job_post.sub_category_id) if job_post.sub_category_id else None
            ),
            "industry_type_id": (
                str(job_post.industry_type_id) if job_post.industry_type_id else None
            ),
            "tier": job_post.tier,
            "description": job_post.description,
            "latitude": point.y if point else None,
            "longitude": point.x if point else None,
            "work_address": job_post.work_address,
            "nearby_landmark": job_post.nearby_landmark,
            "scheduled_start_datetime": job_post.scheduled_start_datetime,
            "scheduled_end_datetime": job_post.scheduled_end_datetime,
            "scheduled_duration": job_post.scheduled_duration,
            "duration_type": job_post.duration_type,
            "shift": job_post.shift,
            "workers": job_post.workers,
            "experience_required": job_post.experience_required,
            "wage": job_post.wage,
            "expected_total": job_post.expected_total,
            "name": job_post.name,
            "country_code": job_post.country_code,
            "phone_number": job_post.phone_number,
            "email": job_post.email,
            "language_preference": job_post.language_preference,
            "tool_provided": job_post.tool_provided,
            "tool_details": job_post.tool_details,
            "special_instructions": job_post.special_instructions,
            "status": job_post.status,
            "is_active": job_post.is_active,
            "assigned_worker_id": (
                str(job_post.assigned_worker_id) if job_post.assigned_worker_id else None
            ),
            "posted_at": job_post.posted_at,
            "assigned_at": job_post.assigned_at,
            "started_at": job_post.started_at,
            "completed_at": job_post.completed_at,
            "cancelled_at": job_post.cancelled_at,
            "created_at": job_post.created_at,
            "updated_at": job_post.updated_at,
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching job details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching job details",
        )
