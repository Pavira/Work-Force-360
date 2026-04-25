import logging
from uuid import UUID

from fastapi import HTTPException, status
from geoalchemy2.shape import to_shape
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, selectinload

from app.models.company_models import CompanyModel
from app.models.industry_skill_models import IndustryTypeModel

VALID_SEARCH_TYPES = {"company_name", "phone", "email"}
logger = logging.getLogger(__name__)


def _build_company_status_query(db: Session, target_status: str):
    return db.query(
        CompanyModel.id,
        CompanyModel.company_name,
        CompanyModel.contact_person_name,
        CompanyModel.contact_phone,
        CompanyModel.auth_phone,
        CompanyModel.status,
    ).filter(
        CompanyModel.status == target_status,
        CompanyModel.is_active.is_(True),
    )


def _apply_search_filters(query, search_term: str | None, search_type: str | None):
    if search_term is None or not search_term.strip():
        return query

    normalized_term = search_term.strip()

    if search_type not in VALID_SEARCH_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid search_type. Allowed values: company_name, phone, email",
        )

    term = f"%{normalized_term}%"
    if search_type == "company_name":
        return query.filter(CompanyModel.company_name.ilike(term))
    if search_type == "phone":
        # Search both auth and contact phone fields to support existing records.
        return query.filter(
            or_(
                CompanyModel.auth_phone.ilike(term),
                CompanyModel.contact_phone.ilike(term),
            )
        )
    return query.filter(CompanyModel.contact_email.ilike(term))


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
        db.query(CompanyModel.status, func.count(CompanyModel.id))
        .filter(
            CompanyModel.is_active.is_(True),
            CompanyModel.status.in_(["approved", "unapproved", "draft"]),
        )
        .group_by(CompanyModel.status)
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


def _paginate_company_query(query, page: int, page_size: int, cursor: str | None):
    ordered_query = query.order_by(CompanyModel.id.asc())
    parsed_cursor = _safe_parse_cursor(cursor)

    if parsed_cursor is not None:
        rows = (
            ordered_query.filter(CompanyModel.id > parsed_cursor).limit(page_size).all()
        )
        next_cursor = str(rows[-1].id) if len(rows) == page_size else None
        prev_cursor = str(rows[0].id) if rows else None
        # Cursor mode is forward-only; page number is not meaningful.
        resolved_page = 1
        return rows, resolved_page, next_cursor, prev_cursor

    offset = (page - 1) * page_size
    rows = ordered_query.offset(offset).limit(page_size).all()
    return rows, page, None, None


def _serialize_company_rows(rows) -> list[dict]:
    items = []
    for row in rows:
        items.append(
            {
                "id": str(row.id),
                "company_name": row.company_name,
                "contact_person_name": row.contact_person_name,
                "phone": row.contact_phone or row.auth_phone,
                "status": row.status,
            }
        )
    return items


def _build_company_total_count_query(db: Session, target_status: str):
    return db.query(func.count(CompanyModel.id)).filter(
        CompanyModel.status == target_status,
        CompanyModel.is_active.is_(True),
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

    if search_type == "company_name":
        return query.filter(CompanyModel.company_name.ilike(term))
    if search_type == "phone":
        return query.filter(
            or_(
                CompanyModel.auth_phone.ilike(term),
                CompanyModel.contact_phone.ilike(term),
            )
        )
    if search_type == "email":
        return query.filter(CompanyModel.contact_email.ilike(term))
    return query


def _get_companies_by_status_service(
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

    query = _build_company_status_query(db=db, target_status=target_status)
    query = _apply_search_filters(
        query=query,
        search_term=search_term,
        search_type=search_type,
    )

    total_count_query = _build_company_total_count_query(
        db=db, target_status=target_status
    )
    total_count_query = _apply_search_filters_to_count_query(
        query=total_count_query,
        search_term=search_term,
        search_type=search_type,
    )
    total_count = total_count_query.scalar() or 0

    rows, resolved_page, next_cursor, prev_cursor = _paginate_company_query(
        query=query,
        page=page,
        page_size=page_size,
        cursor=cursor,
    )
    items = _serialize_company_rows(rows)

    return {
        "items": items,
        "total_count": total_count,
        "page": resolved_page,
        "page_size": page_size,
        "next_cursor": next_cursor,
        "prev_cursor": prev_cursor,
        **_get_status_counts(db=db),
    }


# -----------------------Get All Approved Company details Service----------------------- #
def get_all_approved_companies_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_companies_by_status_service(
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
        logger.exception("Error fetching approved company details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching approved company details",
        )


# -----------------------End Get All Approved Company details Service----------------------- #


# -----------------------Get All Unapproved Company details Service----------------------- #
def get_all_unapproved_companies_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_companies_by_status_service(
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
        logger.exception("Error fetching unapproved company details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching unapproved company details",
        )


# -----------------------End Get All Unapproved Company details Service----------------------- #


# -----------------------Get All Draft Company details Service----------------------- #
def get_all_draft_companies_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    cursor: str | None = None,
    search_term: str | None = None,
    search_type: str | None = None,
) -> dict:
    try:
        return _get_companies_by_status_service(
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
        logger.exception("Error fetching draft company details")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching draft company details",
        )


# -----------------------End Get All Draft Company details Service----------------------- #


# -----------------------Get Company Details by ID Service----------------------- #
def get_company_details_by_id_service(db: Session, company_id: str):
    try:
        company = (
            db.query(CompanyModel)
            .options(
                selectinload(CompanyModel.addresses),
                selectinload(CompanyModel.bank_details),
                selectinload(CompanyModel.documents),
            )
            .filter(CompanyModel.id == company_id, CompanyModel.is_active.is_(True))
            .first()
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )

        industry_name = None
        if company.industry_id:
            industry = (
                db.query(IndustryTypeModel.name)
                .filter(IndustryTypeModel.id == company.industry_id)
                .first()
            )
            industry_name = industry[0] if industry else None

        return {
            "id": company.id,
            "firebase_uid": company.firebase_uid,
            "company_name": company.company_name,
            "industry_id": company.industry_id,
            "industry_name": industry_name,
            "gst_number": company.gst_number,
            "auth_phone": company.auth_phone,
            "contact_person_name": company.contact_person_name,
            "contact_country_code": company.contact_country_code,
            "contact_phone": company.contact_phone,
            "contact_email": company.contact_email,
            "logo_url": company.logo_url,
            "status": company.status,
            "status_approval_message_shown": company.status_approval_message_shown,
            "is_verified": company.is_verified,
            "is_active": company.is_active,
            "addresses": [
                {
                    "id": addr.id,
                    "address": addr.address,
                    "unit_name": addr.unit_name,
                    "city": addr.city,
                    "state": addr.state,
                    "pincode": addr.pincode,
                    "latitude": to_shape(addr.location).y if addr.location else None,
                    "longitude": to_shape(addr.location).x if addr.location else None,
                }
                for addr in company.addresses
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
                for bank in company.bank_details
            ],
            "documents": [
                {
                    "id": doc.id,
                    "document_type": doc.document_type,
                    "document_url": doc.document_url,
                }
                for doc in company.documents
            ],
            "created_at": company.created_at,
            "updated_at": company.updated_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching company details",
        )


# -----------------------End Get Company Details by ID Service----------------------- #


# -----------------------Update Company Status to Approved Service----------------------- #
def update_company_status_to_approved_service(company_id: UUID, db: Session):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        was_approved = company.status == "approved"
        company.status = "approved"
        if not was_approved:
            company.status_approval_message_shown = False
        db.flush()
        return company

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating company status to approved",
        )


# -----------------------End Update Company Status to Approved Service----------------------- #


#  -----------------------Update Company Status to UnApproved Service----------------------- #
def update_company_status_to_unapproved_service(company_id: UUID, db: Session):
    try:
        company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        company.status = "unapproved"
        company.status_approval_message_shown = False
        db.flush()
        return company

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating company status to unapproved",
        )


#  -----------------------End Update Company Status to UnApproved Service----------------------- #
