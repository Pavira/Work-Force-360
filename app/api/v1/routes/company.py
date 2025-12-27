from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session

from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.utils.response import custom_response
from app.schemas.company_schema import CompanyRegistrationSchema
from app.services.company_service import create_company_profile_service
from app.core.limiter import limiter

router = APIRouter()


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
    # current_user: dict = Depends(get_current_user),
):
    """
    Create a new company profile (Firebase authenticated) .
    """
    try:
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

    except Exception as e:
        return custom_response(
            success=False,
            message="Failed to create company",
            data={"error": str(e)},
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
