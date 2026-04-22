import logging
from uuid import UUID

from fastapi import HTTPException, status
from geoalchemy2.shape import to_shape
from sqlalchemy import String, and_, case, func, or_
from sqlalchemy.orm import Session

from app.models.company_models import CompanyModel
from app.models.industry_skill_models import (
    CategorySkillModel,
    IndustryTypeModel,
    SubCategorySkillModel,
)
from app.models.job_model import JobPostingModel
from app.models.worker_models import WorkerRegistrationModel, WorkerSubCategoryModel
from app.services.matching_service import find_matching_workers

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
    return query.filter(
        func.cast(JobPostingModel.assigned_worker_id, String).ilike(term)
    )


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
        rows = (
            ordered_query.filter(JobPostingModel.id > parsed_cursor)
            .limit(page_size)
            .all()
        )
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
        return query.filter(
            func.cast(JobPostingModel.assigned_worker_id, String).ilike(term)
        )
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


# -----------------------Get Job Details By ID--------------------- #
def get_job_details_by_id_service(db: Session, job_id: str) -> dict:
    try:
        try:
            parsed_job_id = UUID(job_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid job_id format. Expected UUID string.",
            ) from exc

        result = (
            db.query(
                JobPostingModel,
                CompanyModel.company_name.label("company_name"),
                CategorySkillModel.name.label("skill_category_name"),
                SubCategorySkillModel.name.label("sub_category_name"),
                IndustryTypeModel.name.label("industry_type_name"),
                WorkerRegistrationModel.name.label("assigned_worker_name"),
            )
            .outerjoin(
                CompanyModel,
                and_(
                    CompanyModel.id == JobPostingModel.company_id,
                    CompanyModel.is_active.is_(True),
                ),
            )
            .outerjoin(
                CategorySkillModel,
                and_(
                    CategorySkillModel.id == JobPostingModel.skill_category_id,
                    CategorySkillModel.is_active.is_(True),
                ),
            )
            .outerjoin(
                SubCategorySkillModel,
                and_(
                    SubCategorySkillModel.id == JobPostingModel.sub_category_id,
                    SubCategorySkillModel.is_active.is_(True),
                ),
            )
            .outerjoin(
                IndustryTypeModel,
                and_(
                    IndustryTypeModel.id == JobPostingModel.industry_type_id,
                    IndustryTypeModel.is_active.is_(True),
                ),
            )
            .outerjoin(
                WorkerRegistrationModel,
                and_(
                    WorkerRegistrationModel.id == JobPostingModel.assigned_worker_id,
                    WorkerRegistrationModel.is_active.is_(True),
                ),
            )
            .filter(
                JobPostingModel.id == parsed_job_id,
                JobPostingModel.is_active.is_(True),
            )
            .first()
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job post not found",
            )

        job_post = result[0]
        point = to_shape(job_post.location) if job_post.location else None
        return {
            "id": str(job_post.id),
            "company_id": str(job_post.company_id) if job_post.company_id else None,
            "company_name": result.company_name,
            "skill_category_id": (
                str(job_post.skill_category_id) if job_post.skill_category_id else None
            ),
            "skill_category_name": result.skill_category_name,
            "sub_category_id": (
                str(job_post.sub_category_id) if job_post.sub_category_id else None
            ),
            "sub_category_name": result.sub_category_name,
            "industry_type_id": (
                str(job_post.industry_type_id) if job_post.industry_type_id else None
            ),
            "industry_type_name": result.industry_type_name,
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
                str(job_post.assigned_worker_id)
                if job_post.assigned_worker_id
                else None
            ),
            "assigned_worker_name": result.assigned_worker_name,
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


# -----------------------End Get Job Details By ID--------------------- #


# ------------------------Get All Nearest Workers List Service----------------------- #
def get_all_nearest_workers_service(
    db: Session,
    job_id: str,
    limit: int = 50,
) -> list[dict]:
    try:
        try:
            parsed_job_id = UUID(job_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid job_id format. Expected UUID string.",
            ) from exc

        if limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limit must be greater than or equal to 1",
            )
        if limit > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limit must be less than or equal to 200",
            )

        job = (
            db.query(JobPostingModel)
            .filter(
                JobPostingModel.id == parsed_job_id,
                JobPostingModel.is_active.is_(True),
            )
            .first()
        )
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job post not found",
            )
        if not job.sub_category_id:
            return []
        if not job.location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job location is required to fetch nearest workers",
            )

        distance_expr = func.ST_Distance(
            WorkerRegistrationModel.location,
            job.location,
        )
        availability_priority_expr = case(
            (
                or_(
                    WorkerRegistrationModel.is_available.is_(True),
                    WorkerRegistrationModel.is_online.is_(True),
                ),
                1,
            ),
            else_=0,
        )
        rows = (
            db.query(
                WorkerRegistrationModel.id,
                WorkerRegistrationModel.name,
                WorkerRegistrationModel.auth_number,
                WorkerRegistrationModel.is_online,
                WorkerRegistrationModel.is_available,
                WorkerSubCategoryModel.sub_category_skill_id,
                distance_expr.label("distance_meters"),
            )
            .join(
                WorkerSubCategoryModel,
                WorkerSubCategoryModel.worker_id == WorkerRegistrationModel.id,
            )
            .filter(
                WorkerRegistrationModel.is_active.is_(True),
                WorkerRegistrationModel.location.isnot(None),
                WorkerSubCategoryModel.sub_category_skill_id == job.sub_category_id,
            )
            .order_by(availability_priority_expr.desc(), distance_expr.asc())
            .limit(limit)
            .all()
        )

        return [
            {
                "worker_id": str(row.id),
                "worker_name": row.name,
                "phone_number": row.auth_number,
                "is_online": row.is_online,
                "is_available": row.is_available,
                "sub_category_id": (
                    str(row.sub_category_skill_id)
                    if row.sub_category_skill_id
                    else None
                ),
                "distance_meters": (
                    int(row.distance_meters)
                    if row.distance_meters is not None
                    else None
                ),
            }
            for row in rows
        ]
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching nearest worker details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching nearest worker details",
        )


# ------------------------End Get All Nearest Workers List Service----------------------- #
