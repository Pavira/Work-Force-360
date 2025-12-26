from sqlalchemy.ext.asyncio import AsyncSession

from app.models.worker_models import WorkerRegistrationModel
from app.schemas.user_schema import WorkerRegistrationSchema


async def create_worker_service(worker: WorkerRegistrationSchema, db: AsyncSession):
    """
    Service function to create a new worker registration entry.
    """
    reg = WorkerRegistrationModel(
        user_id=worker.user_id,
        phone_number=worker.phone_number,
        name=worker.name,
        address=worker.address,
        aadhaar_url=worker.aadhaar_url,
        pan_url=worker.pan_url,
        certificate_url=worker.certificate_url,
        profile_pic_url=worker.profile_pic_url,
        skill_category=worker.skill_category,
        sub_category=worker.sub_category,
        role_type=worker.role_type,
        years=worker.years,
        months=worker.months,
        agreed=worker.agreed,
        created_at=worker.created_at,
        skills=worker.skills,
        location=worker.location,
    )

    db.add(reg)
    await db.commit()
    await db.refresh(reg)
    return reg
