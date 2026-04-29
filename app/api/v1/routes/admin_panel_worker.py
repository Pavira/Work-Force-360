from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.firebase_auth import initialize_firebase
from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.company_schema import UploadUrlRequest
from app.schemas.worker_schema import WorkerRegistrationSchema
from app.services.admin_panel_worker_service import (
    get_all_approved_workers_service,
    get_all_draft_workers_service,
    get_all_unapproved_workers_service,
    get_worker_details_by_id_service,
    update_worker_status_to_approved_service,
    update_worker_status_to_unapproved_service,
)
from app.utils.response import custom_response
from firebase_admin import auth
from app.services.worker_service import (
    create_worker_service,
    generate_upload_url_service,
)

router = APIRouter()


# -----------------------Get All Approved Workers----------------------- #
@router.get(
    "/approved",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_approved_workers(
    request: Request,  # REQUIRED by SlowAPI
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get approved and active workers with backend pagination.
    """
    worker_details = get_all_approved_workers_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Approved worker details and counts fetched successfully",
        data=worker_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Approved Workers----------------------- #


# -----------------------Get All Unapproved Workers----------------------- #
@router.get(
    "/unapproved",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_unapproved_workers(
    request: Request,  # REQUIRED by SlowAPI
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get unapproved and active workers with backend pagination.
    """
    worker_details = get_all_unapproved_workers_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Unapproved worker details and counts fetched successfully",
        data=worker_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Unapproved Workers----------------------- #


# -----------------------Get All Draft Workers----------------------- #
@router.get(
    "/draft",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_draft_workers(
    request: Request,  # REQUIRED by SlowAPI
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    cursor: str | None = Query(None),
    search_term: str | None = Query(None),
    search_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get draft and active workers with backend pagination.
    """
    worker_details = get_all_draft_workers_service(
        db=db,
        page=page,
        page_size=page_size,
        cursor=cursor,
        search_term=search_term,
        search_type=search_type,
    )

    return custom_response(
        success=True,
        message="Draft worker details and counts fetched successfully",
        data=worker_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Draft Workers----------------------- #


# -----------------------Get Worker Details by ID----------------------- #
@router.get(
    "/{worker_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_worker_details_by_id(
    request: Request,
    worker_id: str,
    db: Session = Depends(get_db),
):
    """
    Get worker with full details (basic + skills + bank details + documents)
    """
    worker = get_worker_details_by_id_service(db=db, worker_id=worker_id)

    return custom_response(
        success=True,
        message="Worker details fetched successfully",
        data=worker,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get Worker Details by ID----------------------- #


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


# -----------------------Update Worker Status to Unapproved----------------------- #
@router.patch(
    "/unapprove/{worker_id}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def unapprove_worker(
    request: Request,  # REQUIRED by SlowAPI
    worker_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Update worker status to unapproved.
    """
    worker_db = update_worker_status_to_unapproved_service(
        worker_id=worker_id,
        db=db,
    )

    return custom_response(
        success=True,
        message="Worker profile unapproved successfully",
        data={
            "id": worker_db.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Worker Status to Unapproved----------------------- #


# -----------------------Create Worker Firebase User----------------------- #
class CreateWorkerFirebaseUserRequest(BaseModel):
    phone_number: str


@router.post(
    "/create-worker-firebase-user",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def create_worker_firebase_user(
    request: Request,
    body: CreateWorkerFirebaseUserRequest,
    db: Session = Depends(get_db),
):
    """
    Create a Firebase user with phone number for worker authentication.
    """
    try:
        initialize_firebase()
        user = auth.create_user(phone_number=body.phone_number)
        return custom_response(
            success=True,
            message="Firebase user created successfully",
            data={
                "firebase_uid": user.uid,
                "phone_number": user.phone_number,
            },
            code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Firebase user: {str(e)}",
        )


# -----------------------End Create Worker Firebase User----------------------- #


# -----------------------Generate S3 Upload URL----------------------- #
@router.put("/documents/upload-url")
@limiter.limit("30/minute")
def generate_upload_url(
    request: Request,  # REQUIRED by SlowAPI
    payload: UploadUrlRequest,
    firebase_uid: str,
):

    urls = generate_upload_url_service(
        file_type=payload.file_type, current_user=firebase_uid
    )

    return custom_response(
        success=True,
        message="Upload URL generated successfully",
        data=urls,
        code=status.HTTP_200_OK,
    )


# -----------------------End Generate S3 Upload URL----------------------- #


# -----------------------Create New Worker----------------------- #
@router.post(
    "/create_new_worker",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def create_new_worker(
    request: Request,
    body: WorkerRegistrationSchema,
    firebase_uid: str,
    db: Session = Depends(get_db),
):
    """
    Create a new worker with all details.
    """
    worker_db = create_worker_service(
        db=db,
        worker=body,
        firebase_uid=firebase_uid,
    )

    return custom_response(
        success=True,
        message="Worker created successfully",
        data={
            # "id": worker_db.id,
        },
        code=status.HTTP_201_CREATED,
    )
