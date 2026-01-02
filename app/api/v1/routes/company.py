from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session

from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.models.company_models import Company
from app.utils.response import custom_response
from app.schemas.company_schema import CompanyRegistrationSchema
from app.services.company_service import create_company_profile_service
from app.core.limiter import limiter

router = APIRouter()


# -----------------------Create Company Profile----------------------- #
@router.post(
    "/create_company_profile",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(
    "5/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
async def create_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    company: CompanyRegistrationSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new company profile (Firebase authenticated) .
    """
    company_db = await create_company_profile_service(
        company=company,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company created successfully",
        data={
            "id": company_db.id,
            "company_name": company_db.company_name,
            "status": company_db.status,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Create Company Profile----------------------- #


# -----------------------Get Company Profile----------------------- #
@router.get(
    "/get_company_profile",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
async def get_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    current_user: str = id,
    db: Session = Depends(get_db),
):
    """
    Get company profile (Firebase authenticated).
    """
    company_db = db.query(Company).filter(Company.id == current_user).first()

    return custom_response(
        success=True,
        message="Company profile fetched successfully",
        data={
            # Show full model data
            "id": company_db.id,
            "firebase_uid": company_db.firebase_uid,
            "company_name": company_db.company_name,
            "industry": company_db.industry,
            "gst_number": company_db.gst_number,
            "contact_person_name": company_db.contact_person_name,
            "phone": company_db.phone,
            "email": company_db.email,
            "logo_url": company_db.logo_url,
            "status": company_db.status,
            "is_verified": company_db.is_verified,
            "is_active": company_db.is_active,
            "created_at": company_db.created_at,
        },
        code=status.HTTP_200_OK,
    )
