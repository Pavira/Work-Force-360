from fastapi import APIRouter, Query, Request, Response, status, Depends
from sqlalchemy.orm import Session
from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.core.limiter import limiter
from app.services.admin_panel_company_service import (
    get_all_approved_companies_service,
    get_all_draft_companies_service,
    get_all_unapproved_companies_service,
    get_company_details_by_id_service,
    update_company_status_to_approved_service,
    update_company_status_to_unapproved_service,
)
from app.utils.response import custom_response
from uuid import UUID


router = APIRouter()


# -----------------------Get All Approved Companies----------------------- #
@router.get(
    "/approved",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_approved_companies(
    request: Request,  # REQUIRED by SlowAPI
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get approved and active companies with backend pagination.
    """
    company_details = get_all_approved_companies_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Approved company details and counts fetched successfully",
        data=company_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Approved Companies----------------------- #


# -----------------------Get All Unapproved Companies----------------------- #
@router.get(
    "/unapproved",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_unapproved_companies(
    request: Request,  # REQUIRED by SlowAPI
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get unapproved and active companies with backend pagination.
    """
    company_details = get_all_unapproved_companies_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Unapproved company details and counts fetched successfully",
        data=company_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Unapproved Companies----------------------- #


# -----------------------Get All Draft Companies----------------------- #
@router.get(
    "/draft",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_draft_companies(
    request: Request,  # REQUIRED by SlowAPI
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get draft and active companies with backend pagination.
    """
    company_details = get_all_draft_companies_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Draft company details and counts fetched successfully",
        data=company_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Draft Companies----------------------- #


# -----------------------Get Company Details by ID----------------------- #
@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_company_details_by_id(
    request: Request,
    company_id: str,
    db: Session = Depends(get_db),
):
    """
    Get company with full details (basic + addresses + bank details + documents)
    """
    company = get_company_details_by_id_service(db=db, company_id=company_id)

    return custom_response(
        success=True,
        message="Company details fetched successfully",
        data=company,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get Company Details by ID----------------------- #


# -----------------------Update Company Status to Approved----------------------- #
@router.patch(
    "/approve_company_profile/{company_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def approve_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Update company status to approved (Firebase authenticated) .
    """
    company_db = update_company_status_to_approved_service(
        company_id=company_id,
        db=db,
    )

    return custom_response(
        success=True,
        message="Company profile approved successfully",
        data={
            "id": company_db.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Company Status to Approved----------------------- #


# -----------------------Update Company Status to Unapproved----------------------- #
@router.patch(
    "/unapprove/{company_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def unapprove_company(
    request: Request,  # REQUIRED by SlowAPI
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Update company status to unapproved (Firebase authenticated) .
    """
    company_db = update_company_status_to_unapproved_service(
        company_id=company_id,
        db=db,
    )

    return custom_response(
        success=True,
        message="Company profile unapproved successfully",
        data={
            "id": company_db.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Company Status to Unapproved----------------------- #
