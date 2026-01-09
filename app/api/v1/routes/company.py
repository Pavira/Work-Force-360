from uuid import uuid4
from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.orm import Session
from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.core.limiter import limiter

from app.utils.response import custom_response
from app.schemas.company_schema import (
    CompanyDocumentCreateSchema,
    CompanyInfoSchema,
    CompanyProfileUpdateSchema,
    ContactInfoSchema,
    DocumentInfoSchema,
    UploadUrlRequest,
)
from app.services.company_service import (
    create_company_profile_service,
    generate_upload_url_service,
    get_company_profile_service,
    get_terms_and_conditions,
    save_document_service,
    update_company_profile_service,
    update_contact_info_service,
    update_document_info_service,
)


router = APIRouter()


# -----------------------Company exist or not------------------------ #
@router.get(
    "/company_exists",
    status_code=status.HTTP_200_OK,
)
def company_exists(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Check if company profile exists (Firebase authenticated).
    """
    company_db = get_company_profile_service(firebase_uid=current_user["uid"], db=db)

    if not company_db:
        return custom_response(
            success=True,
            message="Company profile not found",
            data={"exists": False},
            code=status.HTTP_200_OK,
        )

    return custom_response(
        success=True,
        message="Company profile found",
        data={
            "exists": True,
            "id": company_db.id,
            "company_name": company_db.company_name,
            "status": company_db.status,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Company exist or not----------------------- #


# -----------------------Create Company Profile----------------------- #
@router.post(
    "/create_company_profile",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(
    "5/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def create_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    company: CompanyInfoSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new company profile (Firebase authenticated) .
    """
    company_db = create_company_profile_service(
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


# -----------------------Update Contact Person Info----------------------- #
@router.patch(
    "/update_contact_info",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(
    "5/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def update_contact_info(
    request: Request,  # REQUIRED by SlowAPI
    company: ContactInfoSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update contact person info for company profile (Firebase authenticated) .
    """
    company_db = update_contact_info_service(
        contact_info=company,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Contact info updated successfully",
        data={
            "contact_person_name": company_db.contact_person_name,
            # "company_name": company_db.company_person_name,
            # "status": company_db.status,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Update Contact Person Info----------------------- #


# -----------------------Update Document Info----------------------- #
@router.patch(
    "/update_document_info",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(
    "5/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def update_document_info(
    request: Request,  # REQUIRED by SlowAPI
    company: DocumentInfoSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update document info for company profile (Firebase authenticated) .
    """
    company_db = update_document_info_service(
        company=company,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Document info updated successfully",
        data={
            # "id": company_db.id,
            # "company_name": company_db.company_person_name,
            # "status": company_db.status,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Update Document Info----------------------- #


# -----------------------Get Company Profile Route----------------------- #
@router.get(
    "/get_company_profile",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    current_user: str = Depends(get_current_user),
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


# -----------------------End Get Company Profile Route----------------------- #


# -----------------------Update Company Profile Route----------------------- #
@router.patch(
    "/update_company_profile",
    status_code=status.HTTP_201_CREATED,
)
def update_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    company_profile: CompanyProfileUpdateSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update company profile (Firebase authenticated) .
    """
    company_db = update_company_profile_service(
        update=company_profile,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company profile updated successfully",
        data={
            "id": company_db.id,
            "company_name": company_db.company_name,
            "status": company_db.status,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Update Company Profile Service----------------------- #
# -----------------------Fetch Terms and Conditions----------------------- #
@router.get(
    "/terms",
    status_code=status.HTTP_200_OK,
)
def fetch_terms_and_conditions():
    """
    Fetch latest Terms and Conditions
    """

    html = get_terms_and_conditions()
    return Response(content=html, media_type="text/html")


# -----------------------End Fetch Terms and Conditions----------------------- #


# -----------------------Generate S3 Upload URL----------------------- #


@router.post("/documents/upload-url")
def generate_upload_url(
    payload: UploadUrlRequest,
    current_user=Depends(get_current_user),
):

    urls = generate_upload_url_service(
        file_type=payload.file_type, current_user=current_user["uid"]
    )

    return custom_response(
        success=True,
        message="Upload URL generated successfully",
        data=urls,
        code=status.HTTP_200_OK,
    )


# -----------------------End Generate S3 Upload URL----------------------- #


# -----------------------Save Document----------------------- #
@router.post("/documents")
def save_document(
    payload: CompanyDocumentCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    document = save_document_service(
        payload=payload, current_user=current_user["uid"], db=db
    )

    return custom_response(
        success=True,
        message="Document saved successfully",
        data={"id": document.id, "document_type": document.document_type},
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Save Document----------------------- #
