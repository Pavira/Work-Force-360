import traceback

from fastapi import APIRouter, Depends, Request, status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.firebase_auth import get_current_user
from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.worker_schema import WorkerRegistrationSchema
from app.services.worker_service import create_worker_service
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
