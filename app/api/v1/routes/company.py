from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.core.limiter import limiter

from app.utils.response import custom_response
from app.schemas.company_schema import CompanyRegistrationSchema
from app.services.company_service import (
    create_company_profile_service,
    get_company_profile_service,
)


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


# -----------------------Get Company Profile Route----------------------- #
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
    company_details = get_company_profile_service(
        firebase_uid=current_user["uid"], db=db
    )

    return custom_response(
        success=True,
        message="Company profile fetched successfully",
        data=company_details,
        code=status.HTTP_200_OK,
    )
