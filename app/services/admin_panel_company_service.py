from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status

from app.models.company_models import CompanyModel


# -----------------------Get All Approved Company details Service----------------------- #
def get_all_approved_companies_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    try:
        offset = (page - 1) * page_size
        approved_companies = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        approved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        unapproved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        draft_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        return {
            "approved_companies": approved_companies,
            "approved_companies_count": approved_companies_count,
            "unapproved_companies_count": unapproved_companies_count,
            "draft_companies_count": draft_companies_count,
            "page": page,
            "page_size": page_size,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR ðŸ‘‰", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching approved company details",
        )


# -----------------------End Get All Approved Company details Service----------------------- #


# -----------------------Get All Unapproved Company details Service----------------------- #
def get_all_unapproved_companies_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    try:
        offset = (page - 1) * page_size
        unapproved_companies = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        unapproved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        approved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        draft_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        return {
            "unapproved_companies": unapproved_companies,
            "unapproved_companies_count": unapproved_companies_count,
            "approved_companies_count": approved_companies_count,
            "draft_companies_count": draft_companies_count,
            "page": page,
            "page_size": page_size,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR Ã°Å¸â€˜â€°", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching unapproved company details",
        )


# -----------------------End Get All Unapproved Company details Service----------------------- #


# -----------------------Get All Draft Company details Service----------------------- #
def get_all_draft_companies_service(
    db: Session,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    try:
        offset = (page - 1) * page_size
        draft_companies = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        draft_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "draft",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        approved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "approved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        unapproved_companies_count = (
            db.query(CompanyModel)
            .filter(
                CompanyModel.status == "unapproved",
                CompanyModel.is_active.is_(True),
            )
            .count()
        )

        return {
            "draft_companies": draft_companies,
            "draft_companies_count": draft_companies_count,
            "approved_companies_count": approved_companies_count,
            "unapproved_companies_count": unapproved_companies_count,
            "page": page,
            "page_size": page_size,
        }
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR ÃƒÂ°Ã…Â¸Ã¢â‚¬ËœÃ¢â‚¬Â°", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching draft company details",
        )


# -----------------------End Get All Draft Company details Service----------------------- #


# -----------------------Get Company Details by ID Service----------------------- #
def get_company_details_by_id_service(db: Session, company_id: str):
    try:
        company = (
            db.query(CompanyModel)
            .options(
                selectinload(CompanyModel.addresses),
                selectinload(CompanyModel.bank_details),
                selectinload(CompanyModel.documents),
            )
            .filter(CompanyModel.id == company_id, CompanyModel.is_active.is_(True))
            .first()
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )

        return company
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching company details",
        )


# -----------------------End Get Company Details by ID Service----------------------- #
