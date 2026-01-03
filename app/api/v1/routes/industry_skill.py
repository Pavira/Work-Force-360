from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.core.limiter import limiter
from app.utils.response import custom_response

from app.services.industry_skill_service import get_industry_types_service


router = APIRouter()


# -----------------------Get Industry Type Route ----------------------- #
@router.get(
    "/industry_types",
    status_code=200,
)
@limiter.limit(
    "15/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def get_industry_types(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user),
):
    """
    Get list of industry types.
    """
    industry_types = get_industry_types_service(db=db)
    return custom_response(
        success=True,
        message="Industry types fetched successfully",
        data=industry_types,
        code=status.HTTP_200_OK,
    )
