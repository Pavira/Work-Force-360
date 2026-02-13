import os
import traceback
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException, status
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy.orm import Session

from app.models.worker_models import (
    WorkerDocumentModel,
    WorkerRegistrationModel,
    WorkerSubCategoryModel,
)
from app.schemas.worker_schema import WorkerRegistrationSchema


# Helper function for s3 upload url
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)

objects = s3_client.list_objects_v2(Bucket="workforce360-terms", Prefix="worker_docs/")

print(objects)
# End helper function for s3 upload url

# ------------------------ Worker Registration Service ------------------------ #


def _build_location(latitude: Optional[float], longitude: Optional[float]):
    if latitude is None or longitude is None:
        return None
    return from_shape(Point(longitude, latitude), srid=4326)


def create_worker_service(
    worker: WorkerRegistrationSchema,
    db: Session,
    firebase_uid: str,
) -> dict:
    """
    Service function to create a new worker registration entry.
    """
    try:
        # Validation 1 - Prevent duplicate registration for same firebase_uid
        reg = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.firebase_uid == firebase_uid)
            .first()
        )

        reg = WorkerRegistrationModel(
            firebase_uid=firebase_uid,
            name=worker.name,
            auth_number=worker.authNumber,
            category_id=worker.categoryId,
            category_name=worker.categoryName,
            address=worker.address,
            city=worker.city,
            state=worker.state,
            pincode=worker.pincode,
            location=_build_location(worker.latitude, worker.longitude),
            years=worker.years,
            logo_url=(worker.documentInfo.logoUrl if worker.documentInfo else None),
        )
        db.add(reg)
        db.flush()

        if worker.subCategory:
            for idx, sub_id in enumerate(worker.subCategory.subCategoryIds or []):
                sub_name = None
                if worker.subCategory.subCategoryNames:
                    if idx < len(worker.subCategory.subCategoryNames):
                        sub_name = worker.subCategory.subCategoryNames[idx]
                db.add(
                    WorkerSubCategoryModel(
                        worker_id=reg.id,
                        sub_category_id=sub_id,
                        sub_category_name=sub_name,
                    )
                )

        if worker.documentInfo and worker.documentInfo.documents:
            for doc in worker.documentInfo.documents:
                db.add(
                    WorkerDocumentModel(
                        worker_id=reg.id,
                        document_type=doc.documentType,
                        document_url=doc.documentUrl,
                    )
                )
        db.flush()
        return {"id": str(reg.id), "name": reg.name}

    except HTTPException:
        raise
    except Exception as e:
        print("create_worker_service DB ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating worker registration",
        )


# -----------------------END Worker Registration Service -----------------------


# # -----------------------Generate S3 Upload URL Service----------------------- #
def generate_upload_url_service(
    file_type: str,
    current_user,
) -> dict:
    try:
        allowed_types = ["png", "jpg", "jpeg", "pdf"]
        if file_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type",
            )

        CONTENT_TYPES = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "pdf": "application/pdf",
        }

        key = f"worker_docs/{current_user}/{uuid4()}.{file_type}"

        url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": "workforce360-terms",
                "Key": key,
                "ContentType": CONTENT_TYPES[file_type],
            },
            ExpiresIn=300,  # 5 minutes
        )

        return {
            "upload_url": url,
            "file_url": f"https://workforce360-terms.s3.amazonaws.com/{key}",
        }

    except HTTPException:
        raise
    except Exception as e:
        print("S3 ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating upload URL",
        )


# -----------------------End Generate S3 Upload URL Service----------------------- #
