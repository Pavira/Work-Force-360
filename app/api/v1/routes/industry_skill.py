from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.core.limiter import limiter
from app.utils.response import custom_response

from app.services.industry_skill_service import (
    get_category_skills_service,
    get_industry_types_service,
    get_sub_category_skills_by_category_id_service,
)


router = APIRouter()


# -----------------------Get Industry Type Route ----------------------- #
@router.get(
    "/industry_types",
    status_code=200,
)
@limiter.limit(
    "50/minute"
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


# ------------------------End Get Industry Type Route ---------------------------------------------- #


# -----------------------Get Category skills Route ----------------------- #
@router.get(
    "/category_skills",
    status_code=200,
)
@limiter.limit(
    "50/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def get_category_skills(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
):
    """
    Get list of category skills.
    """
    category_skills = get_category_skills_service(db=db)
    return custom_response(
        success=True,
        message="Category skills fetched successfully",
        data=category_skills,
        code=status.HTTP_200_OK,
    )


# ------------------------End Get Category skills Route ---------------------------------------------- #


# -----------------------Get Sub-Category skills by category id Route ----------------------- #
@router.get(
    "/sub_category_skills/{category_skill_id}",
    status_code=200,
)
@limiter.limit("50/minute")
def get_sub_category_skills_by_category_id(
    category_skill_id: str,
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
):
    """
    Get list of sub-category skills by category skill id.
    """

    sub_category_skills = get_sub_category_skills_by_category_id_service(
        db=db, category_skill_id=category_skill_id
    )
    return custom_response(
        success=True,
        message="Sub-category skills fetched successfully",
        data=sub_category_skills,
        code=status.HTTP_200_OK,
    )
