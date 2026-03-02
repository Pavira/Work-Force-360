import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.firebase_auth import get_current_user
from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.company_schema import UploadUrlRequest
from app.schemas.worker_schema import (
    CategorySelectionSchema,
    WorkerAddressUpdateSchema,
    WorkerBankDetailsSchema,
    WorkerDocumentCreateSchema,
    WorkerLogoUpdateSchema,
    WorkerRegistrationSchema,
    WorkerSkillsUpdateSchema,
)
from app.services.worker_service import (
    add_worker_skill_category_service,
    add_document_against_worker_id_and_type_service,
    create_worker_service,
    create_worker_bank_details_service,
    delete_worker_skill_category_service,
    delete_worker_profile_service,
    generate_upload_url_service,
    get_all_worker_details_service,
    get_worker_documents_by_type_service,
    get_worker_profile_service,
    get_worker_terms_and_conditions,
    update_worker_bank_details_service,
    update_worker_status_to_approved_service,
    update_worker_logo_service,
    update_worker_address_service,
    update_worker_skills_service,
    worker_name_and_status_service,
    worker_profile_exist_service,
)
from app.utils.response import custom_response


router = APIRouter()


# -----------------------Worker exist or not------------------------ #
@router.get("/worker_exists", status_code=status.HTTP_200_OK)
def worker_exists(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Check if worker profile exists (Firebase authenticated).
    """

    worker = worker_profile_exist_service(
        firebase_uid=current_user["uid"],
        db=db,
    )

    if not worker:
        return custom_response(
            success=True,
            message="Worker profile not found",
            data={"exists": False},
            code=status.HTTP_200_OK,
        )

    return custom_response(
        success=True,
        message="Worker profile found",
        data={
            "exists": True,
            "id": worker.id,
            "name": worker.name,
            "status": worker.status,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Worker exist or not----------------------- #


# ------------------------ Worker Registration Route ------------------------
@router.post("/create_worker_registration", status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
def create_worker_registration(
    request: Request,
    worker: WorkerRegistrationSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new worker registration.
    """
    try:
        payload = create_worker_service(
            worker=worker, firebase_uid=current_user["uid"], db=db
        )
    except HTTPException as e:
        print("create_worker_registration HTTPException:", e.detail)
        traceback.print_exc()
        raise
    except Exception as e:
        print("create_worker_registration unexpected error:", str(e))
        traceback.print_exc()
        raise

    return custom_response(
        success=True,
        message="Worker registration created successfully",
        data=payload,
        code=status.HTTP_201_CREATED,
    )


# ------------------------END Worker Registration Route ------------------------


# -----------------------Get All Worker Details----------------------- #
@router.get(
    "/all_worker_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_worker_details(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
):
    """
    Get all worker details.
    """
    worker_details = get_all_worker_details_service(db=db)

    return custom_response(
        success=True,
        message="All worker details fetched successfully",
        data=worker_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Worker Details----------------------- #


# -----------------------Delete Worker Details----------------------- #
@router.delete(
    "/delete_worker/{auth_number}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def delete_worker_details(
    request: Request,  # REQUIRED by SlowAPI
    auth_number: str,
    db: Session = Depends(get_db),
):
    """
    Delete worker details.
    """
    worker_details = delete_worker_profile_service(
        auth_number=auth_number,
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker details deleted successfully",
        data={"id": worker_details.id, "name": worker_details.name},
        code=status.HTTP_200_OK,
    )


# -----------------------End Delete Worker Details----------------------- #


# -----------------------Get Worker Documents based on document type----------------------- #
@router.get(
    "/get_worker_documents_by_type/{document_type}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def get_worker_documents(
    request: Request,  # REQUIRED by SlowAPI
    document_type: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get worker documents based on document type (Firebase authenticated).
    """
    documents = get_worker_documents_by_type_service(
        document_type=document_type,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker documents fetched successfully",
        data={"documents": documents},
        code=status.HTTP_200_OK,
    )


# -----------------------End Get Worker Documents based on document type----------------------- #


# -----------------------Update Worker Profile Logo----------------------- #
@router.patch(
    "/update_worker_logo",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def update_worker_logo(
    request: Request,  # REQUIRED by SlowAPI
    logo_url: WorkerLogoUpdateSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update worker profile logo (Firebase authenticated).
    """
    final_logo_url = logo_url.logoUrl
    if not final_logo_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="logo_url (or logoUrl) is required",
        )

    worker = update_worker_logo_service(
        logo_url=final_logo_url,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker logo updated successfully",
        data={
            "id": worker.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Worker Profile Logo----------------------- #


# -----------------------Add more documents against worker id & document type----------------------- #
@router.post(
    "/add_documents_against_worker_id_and_type",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def add_documents_against_worker_id_and_type(
    request: Request,  # REQUIRED by SlowAPI
    document_info: WorkerDocumentCreateSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Add more documents against worker id & document type (Firebase authenticated).
    """
    document_db = add_document_against_worker_id_and_type_service(
        document_info=document_info,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker document added successfully",
        data={
            "id": document_db.id,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Add more documents against worker id & document type----------------------- #


# -----------------------Get Worker Name and Status----------------------- #
@router.get(
    "/get_worker_name_and_status",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("100/minute")
def get_worker_name_and_status(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get worker name and status (Firebase authenticated).
    """
    worker = worker_name_and_status_service(
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker profile found",
        data={
            "name": worker["name"],
            "logo_url": worker["logoUrl"],
            "status": worker["status"],
            "statusApprovalMessageShown": worker["statusApprovalMessageShown"],
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Get Worker Name and Status----------------------- #


# -----------------------Get Worker Profile Route----------------------- #
@router.get(
    "/get_worker_profile",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_worker_profile(
    request: Request,  # REQUIRED by SlowAPI
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get worker profile (Firebase authenticated).
    """
    worker_details = get_worker_profile_service(firebase_uid=current_user["uid"], db=db)

    return custom_response(
        success=True,
        message="Worker profile fetched successfully",
        data=worker_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get Worker Profile Route----------------------- #


# -----------------------Update Worker Address----------------------- #
@router.patch("/update_worker_address", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def update_worker_address(
    request: Request,  # REQUIRED by SlowAPI
    address: WorkerAddressUpdateSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update worker address (Firebase authenticated).
    """
    worker = update_worker_address_service(
        address=address,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker address updated successfully",
        data={
            "id": worker.id,
            "address": worker.address,
            "city": worker.city,
            "state": worker.state,
            "pincode": worker.pincode,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Worker Address----------------------- #


# -----------------------Update Worker Skills----------------------- #
@router.patch("/update_worker_skills", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def update_worker_skills(
    request: Request,  # REQUIRED by SlowAPI
    skills: WorkerSkillsUpdateSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update worker skill category and sub-category mappings (Firebase authenticated).
    """
    worker = update_worker_skills_service(
        skills=skills,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker skills updated successfully",
        data={
            "id": worker.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Worker Skills----------------------- #


# -----------------------Add Worker Skill Category----------------------- #
@router.post(
    "/add_skill_category_against_worker_id", status_code=status.HTTP_201_CREATED
)
@limiter.limit("30/minute")
def add_skill_category_against_worker_id(
    request: Request,  # REQUIRED by SlowAPI
    category: CategorySelectionSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Add a new skill category (and related sub-categories) for worker (Firebase authenticated).
    """
    payload = add_worker_skill_category_service(
        category=category,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker skill category added successfully",
        data=payload,
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Add Worker Skill Category----------------------- #


# -----------------------Delete Worker Skill Category----------------------- #
@router.delete(
    "/delete_worker_skill_category/{category_id}", status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def delete_worker_skill_category(
    request: Request,  # REQUIRED by SlowAPI
    category_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a worker category and all related worker sub-categories (Firebase authenticated).
    """
    payload = delete_worker_skill_category_service(
        category_id=category_id,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker category deleted successfully",
        data=payload,
        code=status.HTTP_200_OK,
    )


# -----------------------End Delete Worker Skill Category----------------------- #


# -----------------------Create Worker Bank Details----------------------- #
@router.post(
    "/create_worker_bank_details",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def create_worker_bank_details(
    request: Request,  # REQUIRED by SlowAPI
    bank_details: WorkerBankDetailsSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create worker bank details (Firebase authenticated).
    """
    bank_db = create_worker_bank_details_service(
        bank_details=bank_details,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker bank details created successfully",
        data={
            "id": bank_db.id,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Create Worker Bank Details----------------------- #


# -----------------------Update Worker Bank Details----------------------- #
@router.patch(
    "/update_worker_bank_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def update_worker_bank_details(
    request: Request,  # REQUIRED by SlowAPI
    bank_details: WorkerBankDetailsSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update worker bank details (Firebase authenticated).
    """
    bank_db = update_worker_bank_details_service(
        bank_details=bank_details,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker bank details updated successfully",
        data={
            "id": bank_db.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Worker Bank Details----------------------- #


# -----------------------Fetch Worker Terms and Conditions----------------------- #
@router.get(
    "/terms",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def fetch_worker_terms_and_conditions(
    request: Request,  # REQUIRED by SlowAPI
):
    """
    Fetch latest Worker Terms and Conditions.
    """

    html = get_worker_terms_and_conditions()
    return Response(content=html, media_type="text/html")


# -----------------------End Fetch Worker Terms and Conditions----------------------- #

# -----------------------Generate S3 Upload URL----------------------- #


@router.put("/documents/upload-url")
@limiter.limit("30/minute")
def generate_upload_url(
    request: Request,  # REQUIRED by SlowAPI
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


# -----------------------Update Worker Status to Approved----------------------- #
@router.patch(
    "/approve_worker_profile/{worker_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def approve_worker_profile(
    request: Request,  # REQUIRED by SlowAPI
    worker_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Update worker status to approved.
    """
    worker_db = update_worker_status_to_approved_service(
        worker_id=worker_id,
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker profile approved successfully",
        data={
            "id": worker_db.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Worker Status to Approved----------------------- #
