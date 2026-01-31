from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.industry_skill_models import (
    CategorySkillModel,
    IndustryTypeModel,
    SubCategorySkillModel,
)


# -----------------------Get Industry Type Service ----------------------- #
def get_industry_types_service(db: Session) -> list[IndustryTypeModel]:
    """
    Service to get list of industry types.
    """
    # put everthing in try except block
    try:
        industry_types = (
            db.query(IndustryTypeModel)
            .filter(IndustryTypeModel.is_active == True)  # noqa: E712
            .all()
        )
        return industry_types
    except Exception as e:
        print("DB ERROR 👉", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching industry types",
        )


# ------------------------End Get Industry Type Service ---------------------------------------------- #
# -----------------------Get Category Skills Service ----------------------- #
def get_category_skills_service(db: Session) -> list[CategorySkillModel]:
    """
    Service to get list of category skills.
    """
    # put everthing in try except block
    try:
        category_skills = (
            db.query(CategorySkillModel)
            .filter(CategorySkillModel.is_active == True)
            .all()
        )
        return category_skills
    except Exception as e:
        print("DB ERROR 👉", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching category skills",
        )


# ------------------------End Get Category Skills Service ---------------------------------------------- #


# -----------------------Get sub Category skills by category id Service ----------------------- #
def get_sub_category_skills_by_category_id_service(
    db: Session, category_skill_id: str
) -> list[SubCategorySkillModel]:
    """
    Service to get list of sub category skills by category id.
    """
    try:
        sub_category_skills = (
            db.query(SubCategorySkillModel)
            .filter(
                SubCategorySkillModel.category_skill_id == category_skill_id,
                SubCategorySkillModel.is_active == True,
            )
            .all()
        )
        return sub_category_skills
    except Exception as e:
        print("DB ERROR 👉", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching sub category skills",
        )


# ------------------------End Get sub Category skills by category id Service ---------------------------------------------- #
