import traceback
from typing import Optional

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
