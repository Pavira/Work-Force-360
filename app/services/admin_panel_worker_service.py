import logging
import traceback
from uuid import UUID

from fastapi import HTTPException, status
from geoalchemy2.shape import to_shape
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, selectinload

from app.models.industry_skill_models import CategorySkillModel, SubCategorySkillModel
from app.models.worker_models import (
    WorkerBankDetailsModel,
    WorkerDocumentModel,
    WorkerRegistrationModel,
    WorkerSkillCategoryModel,
    WorkerSubCategoryModel,
)
from app.schemas.worker_schema import WorkerRegistrationSchema
from app.schemas.worker_schema import WorkerRegistrationSchema
from app.services.worker_service import _build_location

VALID_SEARCH_TYPES = {"name", "phone"}
logger = logging.getLogger(__name__)


def _build_worker_status_query(db: Session, target_status: str):
    return db.query(
        WorkerRegistrationModel.id,
        WorkerRegistrationModel.name,
        WorkerRegistrationModel.auth_number,
        WorkerRegistrationModel.status,
    ).filter(
        WorkerRegistrationModel.status == target_status,
        WorkerRegistrationModel.is_active.is_(True),
    )


def _apply_search_filters(query, search_term: str | None, search_type: str | None):
    if search_term is None or not search_term.strip():
        return query

    normalized_term = search_term.strip()

    if search_type not in VALID_SEARCH_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid search_type. Allowed values: name, phone",
        )

    term = f"%{normalized_term}%"
    if search_type == "name":
        return query.filter(WorkerRegistrationModel.name.ilike(term))
    return query.filter(
        or_(
            WorkerRegistrationModel.auth_number.ilike(term),
            WorkerRegistrationModel.country_code.ilike(term),
        )
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
        db.query(WorkerRegistrationModel.status, func.count(WorkerRegistrationModel.id))
        .filter(
            WorkerRegistrationModel.is_active.is_(True),
            WorkerRegistrationModel.status.in_(["approved", "unapproved", "draft"]),
        )
        .group_by(WorkerRegistrationModel.status)
        .all()
    )
    status_count_map = {status_name: count for status_name, count in rows}
    return {
        "approved_count": status_count_map.get("approved", 0),
        "unapproved_count": status_count_map.get("unapproved", 0),
        "draft_count": status_count_map.get("draft", 0),
        "total_count": status_count_map.get("approved", 0)
        + status_count_map.get("unapproved", 0)
        + status_count_map.get("draft", 0),
    }


def _paginate_worker_query(query, page: int, page_size: int, cursor: str | None):
    ordered_query = query.order_by(WorkerRegistrationModel.id.asc())
    parsed_cursor = _safe_parse_cursor(cursor)

    if parsed_cursor is not None:
        rows = (
            ordered_query.filter(WorkerRegistrationModel.id > parsed_cursor)
            .limit(page_size)
            .all()
        )
        next_cursor = str(rows[-1].id) if len(rows) == page_size else None
        prev_cursor = str(rows[0].id) if rows else None
        # Cursor mode is forward-only; page number is not meaningful.
        resolved_page = 1
        return rows, resolved_page, next_cursor, prev_cursor

    offset = (page - 1) * page_size
    rows = ordered_query.offset(offset).limit(page_size).all()
    return rows, page, None, None


def _serialize_worker_rows(rows) -> list[dict]:
    items = []
    for row in rows:
        items.append(
            {
                "id": str(row.id),
                "name": row.name,
                "phone": row.auth_number,
                "status": row.status,
            }
        )
    return items


def _build_worker_total_count_query(db: Session, target_status: str):
    return db.query(func.count(WorkerRegistrationModel.id)).filter(
        WorkerRegistrationModel.status == target_status,
        WorkerRegistrationModel.is_active.is_(True),
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

    if search_type == "name":
        return query.filter(WorkerRegistrationModel.name.ilike(term))
    if search_type == "phone":
        return query.filter(
            or_(
                WorkerRegistrationModel.auth_number.ilike(term),
                WorkerRegistrationModel.country_code.ilike(term),
            )
        )
    return query


def _get_workers_by_status_service(
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

    query = _build_worker_status_query(db=db, target_status=target_status)
    query = _apply_search_filters(
        query=query,
        search_term=search_term,
        search_type=search_type,
    )

    total_count_query = _build_worker_total_count_query(
        db=db, target_status=target_status
    )
    total_count_query = _apply_search_filters_to_count_query(
        query=total_count_query,
        search_term=search_term,
        search_type=search_type,
    )
    total_count = total_count_query.scalar() or 0

    rows, resolved_page, next_cursor, prev_cursor = _paginate_worker_query(
        query=query,
        page=page,
        page_size=page_size,
        cursor=cursor,
    )
    items = _serialize_worker_rows(rows)

    return {
        "items": items,
        # "total_count": total_count,
        "page": resolved_page,
        "page_size": page_size,
        "next_cursor": next_cursor,
        "prev_cursor": prev_cursor,
        **_get_status_counts(db=db),
    }


# -----------------------Get All Approved Worker details Service----------------------- #
def get_all_approved_workers_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_workers_by_status_service(
            db=db,
            target_status="approved",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching approved worker details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching approved worker details",
        )


# -----------------------End Get All Approved Worker details Service----------------------- #


# -----------------------Get All Unapproved Worker details Service----------------------- #
def get_all_unapproved_workers_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_workers_by_status_service(
            db=db,
            target_status="unapproved",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching unapproved worker details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching unapproved worker details",
        )


# -----------------------End Get All Unapproved Worker details Service----------------------- #


# -----------------------Get All Draft Worker details Service----------------------- #
def get_all_draft_workers_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_workers_by_status_service(
            db=db,
            target_status="draft",
            page=page,
            page_size=page_size,
            cursor=cursor,
            search_term=search_term,
            search_type=search_type,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching draft worker details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching draft worker details",
        )


# -----------------------End Get All Draft Worker details Service----------------------- #


def admin_create_worker_service(
    worker: WorkerRegistrationSchema,
    db: Session,
    firebase_uid: str,
) -> dict:
    """
    Service function to create a new worker registration entry.
    """
    try:
        # Prevent duplicate registration
        existing = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.firebase_uid == firebase_uid)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Worker already registered",
            )

        reg = WorkerRegistrationModel(
            firebase_uid=firebase_uid,
            name=worker.name,
            country_code=worker.countryCode,
            auth_number=worker.authNumber,
            address=worker.address,
            city=worker.city,
            state=worker.state,
            pincode=worker.pincode,
            location=_build_location(worker.latitude, worker.longitude),
            logo_url=(worker.documentInfo.logoUrl if worker.documentInfo else None),
        )
        db.add(reg)
        db.flush()

        # ----------------------------
        # Handle Skills (Professional)
        # ----------------------------
        for category in worker.categories:

            # Insert category with experience
            worker_category = WorkerSkillCategoryModel(
                worker_id=reg.id,
                category_skill_id=category.categoryId,
                experience_years=category.experienceYears,
            )

            db.add(worker_category)
            # Validate subcategories belong to this category
            if category.subCategoryIds:

                valid_subs = (
                    db.query(SubCategorySkillModel.id)
                    .filter(
                        SubCategorySkillModel.id.in_(category.subCategoryIds),
                        SubCategorySkillModel.category_skill_id == category.categoryId,
                    )
                    .all()
                )

                valid_sub_ids = {str(v[0]) for v in valid_subs}

                for sub_id in category.subCategoryIds:
                    if sub_id not in valid_sub_ids:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid subcategory for selected category",
                        )

                    db.add(
                        WorkerSubCategoryModel(
                            worker_id=reg.id,
                            sub_category_skill_id=sub_id,
                        )
                    )
        # ----------------------------
        # Documents
        # ----------------------------
        if worker.documentInfo and worker.documentInfo.documents:
            for doc in worker.documentInfo.documents:
                db.add(
                    WorkerDocumentModel(
                        worker_id=reg.id,
                        document_type=doc.documentType,
                        document_url=doc.documentUrl,
                    )
                )

        # ----------------------------
        # Bank Details
        # ----------------------------
        if worker.bankDetails:
            db.add(
                WorkerBankDetailsModel(
                    worker_id=reg.id,
                    bank_name=worker.bankDetails.bankName,
                    account_number=worker.bankDetails.accountNumber,
                    ifsc_code=worker.bankDetails.ifscCode,
                )
            )

        db.add(reg)
        db.flush()
        return {"id": str(reg.id), "name": reg.name}

    except HTTPException:
        raise
    except Exception as e:
        print("create_worker_service DB ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating worker registration",
        )


# -----------------------END Worker Registration Service -----------------------


# -----------------------Get Worker Details by ID Service----------------------- #
def get_worker_details_by_id_service(db: Session, worker_id: str):
    try:
        worker = (
            db.query(WorkerRegistrationModel)
            .options(
                selectinload(WorkerRegistrationModel.categories),
                selectinload(WorkerRegistrationModel.sub_categories),
                selectinload(WorkerRegistrationModel.documents),
                selectinload(WorkerRegistrationModel.bank_details),
            )
            .filter(
                WorkerRegistrationModel.id == worker_id,
                WorkerRegistrationModel.is_active.is_(True),
            )
            .first()
        )

        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found",
            )

        category_ids = [category.category_skill_id for category in worker.categories]
        sub_category_ids = [sub.sub_category_skill_id for sub in worker.sub_categories]

        category_rows = (
            db.query(CategorySkillModel.id, CategorySkillModel.name)
            .filter(CategorySkillModel.id.in_(category_ids))
            .all()
            if category_ids
            else []
        )

        sub_category_rows = (
            db.query(
                SubCategorySkillModel.id,
                SubCategorySkillModel.name,
                SubCategorySkillModel.category_skill_id,
            )
            .filter(SubCategorySkillModel.id.in_(sub_category_ids))
            .all()
            if sub_category_ids
            else []
        )

        category_name_map = {row.id: row.name for row in category_rows}
        sub_category_map = {
            row.id: {"name": row.name, "category_skill_id": row.category_skill_id}
            for row in sub_category_rows
        }

        categories = []
        for category in worker.categories:
            matched_sub_ids = []
            matched_sub_names = []
            for sub in worker.sub_categories:
                sub_data = sub_category_map.get(sub.sub_category_skill_id)
                if not sub_data:
                    continue
                if sub_data["category_skill_id"] == category.category_skill_id:
                    matched_sub_ids.append(str(sub.sub_category_skill_id))
                    matched_sub_names.append(sub_data["name"])

            categories.append(
                {
                    "categoryId": str(category.category_skill_id),
                    "categoryName": category_name_map.get(category.category_skill_id),
                    "experienceYears": category.experience_years,
                    "subCategoryIds": matched_sub_ids,
                    "subCategoryNames": matched_sub_names,
                }
            )

        point = to_shape(worker.location) if worker.location else None

        return {
            "id": str(worker.id),
            "firebase_uid": worker.firebase_uid,
            "name": worker.name,
            "country_code": worker.country_code,
            "auth_number": worker.auth_number,
            "logo_url": worker.logo_url,
            "categories": categories,
            "address": worker.address,
            "city": worker.city,
            "state": worker.state,
            "pincode": worker.pincode,
            "latitude": point.y if point else None,
            "longitude": point.x if point else None,
            "documents": [
                {
                    "id": doc.id,
                    "document_type": doc.document_type,
                    "document_url": doc.document_url,
                }
                for doc in worker.documents
            ],
            "bank_details": [
                {
                    "id": bank.id,
                    "bank_name": bank.bank_name,
                    "account_holder_name": bank.account_holder_name,
                    "account_number": bank.account_number,
                    "ifsc_code": bank.ifsc_code,
                    "upi_id": bank.upi_id,
                }
                for bank in worker.bank_details
            ],
            "status": worker.status,
            "status_approval_message_shown": worker.status_approval_message_shown,
            "is_active": worker.is_active,
            "is_online": worker.is_online,
            "is_available": worker.is_available,
            "current_job_id": worker.current_job_id,
            "created_at": worker.created_at,
            "updated_at": worker.updated_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching worker details",
        )


# -----------------------End Get Worker Details by ID Service----------------------- #


# -----------------------Update Worker Status to Approved Service----------------------- #
def update_worker_status_to_approved_service(worker_id: UUID, db: Session):
    try:
        worker = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.id == worker_id)
            .first()
        )

        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found",
            )

        was_approved = worker.status == "approved"
        worker.status = "approved"
        if not was_approved:
            worker.status_approval_message_shown = False
        db.flush()
        return worker

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR =>", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating worker status to approved",
        )


# -----------------------End Update Worker Status to Approved Service----------------------- #


# -----------------------Update Worker Status to UnApproved Service----------------------- #
def update_worker_status_to_unapproved_service(worker_id: UUID, db: Session):
    try:
        worker = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.id == worker_id)
            .first()
        )

        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found",
            )

        worker.status = "unapproved"
        worker.status_approval_message_shown = False
        db.flush()
        return worker

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR =>", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating worker status to unapproved",
        )


# -----------------------End Update Worker Status to UnApproved Service----------------------- #
