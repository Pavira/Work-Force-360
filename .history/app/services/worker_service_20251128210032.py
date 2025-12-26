from sqlalchemy.orm import Session
from app.models.worker_models import WorkerRegistrationModel
from app.schemas.worker_schema import WorkerRegistrationSchema


async def create_worker_service(worker: WorkerRegistrationSchema, db: Session):
    """
    Service function to create a new worker registration entry.
    """

    reg = WorkerRegistrationModel(
        user_id=worker.userId,
        phone_number=worker.phoneNumber,
        name=worker.name,
        address=worker.address,
        aadhaar_url=worker.aadhaarUrl,
        pan_url=worker.panUrl,
        certificate_url=worker.certificateUrl or [],
        profile_pic_url=worker.profilePicUrl,
        skill_category=worker.skillCategory,
        sub_category=worker.subCategory,
        role_type=worker.roleType,
        years=worker.years,
        months=worker.months,
        agreed=worker.agreed,
        # JSON conversions (IMPORTANT)
        skills=[skill.model_dump() for skill in worker.skills],
        location=worker.location.model_dump() if worker.location else None,
    )

    db.add(reg)
    db.commit()
    db.refresh(reg)

    return reg
