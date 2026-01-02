from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company_models import Company, CompanyAddress, CompanyDocument
from app.schemas.company_schema import CompanyRegistrationSchema


# -----------------------Create Company Profile Service----------------------- #
async def create_company_profile_service(
    company: CompanyRegistrationSchema,
    firebase_uid: str,
    db: Session,
) -> Company:
    try:
        # Prevent duplicate registration
        existing = (
            db.query(Company).filter(Company.firebase_uid == firebase_uid).first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company already registered",
            )

        with db.begin():
            company_db = Company(
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
                    CompanyAddress(
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
                    CompanyDocument(
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
