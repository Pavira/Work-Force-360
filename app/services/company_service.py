from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company import Company, CompanyAddress, CompanyDocument
from app.schemas.company import CompanyRegistrationSchema


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
                company_name=company.company_name,
                industry=company.industry,
                gst_number=company.gst_number,
                contact_person_name=company.contact_person_name,
                email=company.email,
                phone=company.phone,
                logo_url=company.logo_url,
            )
            db.add(company_db)
            db.flush()  # ensures company_db.id exists

            for addr in company.addresses:
                db.add(
                    CompanyAddress(
                        company_id=company_db.id,
                        address=addr.address,
                        unit_name=addr.unit_name,
                        city=addr.city,
                        state=addr.state,
                        pincode=addr.pincode,
                    )
                )

            for doc in company.documents:
                db.add(
                    CompanyDocument(
                        company_id=company_db.id,
                        document_type=doc.document_type,
                        document_url=doc.document_url,
                    )
                )

        return company_db

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database transaction failed",
        )
