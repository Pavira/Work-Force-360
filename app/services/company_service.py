from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company_models import (
    CompanyModel,
    CompanyAddressModel,
    CompanyDocumentModel,
)
from app.schemas.company_schema import CompanyRegistrationSchema


# -----------------------Create Company Profile Service----------------------- #
def create_company_profile_service(
    company: CompanyRegistrationSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        # Validation 1 - Prevent duplicate registration for same firebase_uid
        existing = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company already registered",
            )
        # Validation 2 - Prevent duplicate registration for same email
        existing_emal = (
            db.query(CompanyModel).filter(CompanyModel.email == company.email).first()
        )
        if existing_emal:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered with another company",
            )

        company_db = CompanyModel(
            firebase_uid=firebase_uid,
            # firebase_uid="firebase_uid",
            company_name=company.companyName,
            industry=company.industry,
            gst_number=company.gst,
            contact_person_name=company.contactPersonName,
            email=company.email,
            phone=company.phone,
            logo_url=company.logoUrl,
        )
        db.add(company_db)
        db.flush()  # ensures company_db.id exists
        for addr in company.addresses:
            db.add(
                CompanyAddressModel(
                    company_id=company_db.id,
                    address=addr.address,
                    unit_name=addr.unitName,
                    city=addr.city,
                    state=addr.state,
                    pincode=addr.pincode,
                )
            )
        for doc in company.documents:
            db.add(
                CompanyDocumentModel(
                    company_id=company_db.id,
                    document_type=doc.documentType,
                    document_url=doc.documentUrl,
                )
            )

        return company_db

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database transaction failed",
        )


# -----------------------Get Company Profile Service ----------------------- #
def get_company_profile_service(
    current_user: str,
    db: Session,
) -> CompanyModel:
    try:
        company_profile = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == current_user)
            .first()
        )
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )
        return company_profile
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching company profile",
        )
