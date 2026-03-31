from uuid import UUID

from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status
from app.models.industry_skill_models import IndustryTypeModel
from geoalchemy2.shape import to_shape

from app.models.company_models import CompanyModel


# -----------------------Get All Approved Company details Service----------------------- #
def get_all_approved_companies_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    try:
        offset = (page - 1) * page_size
        approved_companies = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        approved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        unapproved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        draft_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        return {
            "approved_companies": approved_companies,
            "approved_companies_count": approved_companies_count,
            "unapproved_companies_count": unapproved_companies_count,
            "draft_companies_count": draft_companies_count,
            "page": page,
            "page_size": page_size,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR ðŸ‘‰", e)  # or logger.exception(e)
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
) -> dict:
    try:
        offset = (page - 1) * page_size
        unapproved_companies = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        unapproved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        approved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        draft_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        return {
            "unapproved_companies": unapproved_companies,
            "unapproved_companies_count": unapproved_companies_count,
            "approved_companies_count": approved_companies_count,
            "draft_companies_count": draft_companies_count,
            "page": page,
            "page_size": page_size,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR Ã°Å¸â€˜â€°", e)  # or logger.exception(e)
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
) -> dict:
    try:
        offset = (page - 1) * page_size
        draft_companies = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        draft_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        approved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        unapproved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        return {
            "draft_companies": draft_companies,
            "draft_companies_count": draft_companies_count,
            "approved_companies_count": approved_companies_count,
            "unapproved_companies_count": unapproved_companies_count,
            "page": page,
            "page_size": page_size,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR ÃƒÂ°Ã…Â¸Ã¢â‚¬ËœÃ¢â‚¬Â°", e)  # or logger.exception(e)
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
