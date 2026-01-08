from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company_models import (
    CompanyModel,
    CompanyAddressModel,
    CompanyDocumentModel,
)
from app.schemas.company_schema import (
    CompanyInfoSchema,
    CompanyProfileUpdateSchema,
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
    update: CompanyProfileUpdateSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    company = (
        db.query(CompanyModel).filter(CompanyModel.firebase_uid == firebase_uid).first()
    )

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found",
        )

    data = update.model_dump(exclude_unset=True)

    # Simple field updates
    if "companyName" in data:
        company.company_name = data["companyName"]

    if "industryType" in data:
        company.industry = data["industryType"]

    if "gstNo" in data:
        company.gst_number = data["gstNo"]

    # Address update (replace strategy)
    if "addresses" in data:
        db.query(CompanyAddressModel).filter(
            CompanyAddressModel.company_id == company.id
        ).delete(synchronize_session=False)

        for addr in data["addresses"]:
            db.add(
                CompanyAddressModel(
                    company_id=company.id,
                    address=addr["address"],
                    unit_name=addr["unitName"],
                    city=addr["city"],
                    state=addr["state"],
                    pincode=addr["pincode"],
                )
            )
    # Contact Info update
    if "contactInfo" in data:
        ci = data["contactInfo"]

        if "contactPersonName" in ci:
            company.contact_person_name = ci["contactPersonName"]

        if "contactPersonPhone" in ci:
            company.contact_phone = ci["contactPersonPhone"]

        if "contactEmail" in ci:
            exists = (
                db.query(CompanyModel)
                .filter(
                    CompanyModel.contact_email == ci["contactEmail"],
                    CompanyModel.id != company.id,
                )
                .first()
            )
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered with another company",
                )
            company.contact_email = ci["contactEmail"]

    # Document Info update
    if "documentInfo" in data:
        di = data["documentInfo"]

        if "logoUrl" in di:
            company.logo_url = di["logoUrl"]

        if "documents" in di:
            db.query(CompanyDocumentModel).filter(
                CompanyDocumentModel.company_id == company.id
            ).delete(synchronize_session=False)

            for doc in di["documents"]:
                db.add(
                    CompanyDocumentModel(
                        company_id=company.id,
                        document_type=doc.get("documentType"),
                        document_url=doc.get("documentUrl"),
                    )
                )

    db.flush()
    return company


# -----------------------End Update Company Profile Service----------------------- #
