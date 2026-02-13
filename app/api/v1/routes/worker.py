import traceback

from fastapi import APIRouter, Depends, Request, status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.firebase_auth import get_current_user
from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.company_schema import UploadUrlRequest
from app.schemas.worker_schema import WorkerRegistrationSchema
from app.services.worker_service import (
    create_worker_service,
    generate_upload_url_service,
)
from app.utils.response import custom_response


router = APIRouter()


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
