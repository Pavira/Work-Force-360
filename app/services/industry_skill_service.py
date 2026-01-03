from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.industry_skill_models import IndustryTypeModel


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
