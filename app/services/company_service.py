from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company_models import (
    CompanyModel,
    CompanyAddressModel,
    CompanyDocumentModel,
)
from app.schemas.company_schema import (
    CompanyInfoSchema,
    ContactInfoSchema,
    DocumentInfoSchema,
)


# -----------------------Get Company Profile Service ----------------------- #
def get_company_profile_service(
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        return (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching company profile",
        )


# -----------------------End Get Company Profile Service ----------------------- #


# -----------------------Create Company Profile Service----------------------- #
def create_company_profile_service(
    company: CompanyInfoSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        # Validation 1 - Prevent duplicate registration for same firebase_uid
        company_db = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )

        company_db = CompanyModel(
            firebase_uid=firebase_uid,
            company_name=company.companyName,
            industry=company.industryType,
            gst_number=company.gstNo,
            auth_phone=company.authPhone,
        )
        db.add(company_db)
        db.flush()
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

        return company_db

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database transaction failed",
        )


# -----------------------End Create Company Profile Service----------------------- #


# -----------------------Update Contact Info Service----------------------- #
def update_contact_info_service(
    contact_info: ContactInfoSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        company_profile = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )

        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        # Check email uniqueness across other companies
        if contact_info.contactEmail:
            email_exists = (
                db.query(CompanyModel)
                .filter(
                    CompanyModel.contact_email == contact_info.contactEmail,
                    CompanyModel.firebase_uid != firebase_uid,
                )
                .first()
            )
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered with another company",
                )

        # Update fields (industry standard)
        company_profile.contact_person_name = contact_info.contactPersonName
        company_profile.contact_phone = contact_info.contactPersonPhone
        company_profile.contact_email = contact_info.contactEmail

        db.flush()
        return company_profile
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating contact info",
        )


# -----------------------End Update Contact Info Service----------------------- #


# -----------------------Update Document Service----------------------- #
def update_document_info_service(
    contact_info: DocumentInfoSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        company_profile = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        # Update contact info
        company_profile.logo_url = contact_info.logoUrl
        for doc in contact_info.documents:
            db.add(
                CompanyDocumentModel(
                    company_id=company_profile.id,
                    document_type=doc.documentType,
                    document_url=doc.documentUrl,
                )
            )

        db.add(company_profile)
        db.flush()
        return company_profile

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating contact info",
        )


# -----------------------End Update Document Service----------------------- #


# -----------------------Update Company Profile Service----------------------- #
def update_company_profile_service(
    company: CompanyInfoSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        company_profile = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )

        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        # Update fields
        company_profile.company_name = company.companyName
        company_profile.industry = company.industryType
        company_profile.gst_number = company.gstNo

        # Update addresses
        if company.addresses:
            # Clear existing addresses
            db.query(CompanyAddressModel).filter(
                CompanyAddressModel.company_id == company_profile.id
            ).delete()

            for addr in company.addresses:
                db.add(
                    CompanyAddressModel(
                        company_id=company_profile.id,
                        address=addr.address,
                        unit_name=addr.unitName,
                        city=addr.city,
                        state=addr.state,
                        pincode=addr.pincode,
                    )
                )

        db.add(company_profile)
        db.flush()
        return company_profile

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating company profile",
        )


# -----------------------End Update Company Profile Service----------------------- #
