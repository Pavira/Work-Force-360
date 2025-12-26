async def worker_service(worker: WorkerRegistrationSchema, db: AsyncSession):
    """
    Service function to create a new worker registration entry.
    """
    reg = Registration(
        user_id=data.userId,
        phone_number=data.phoneNumber,
        name=data.name,
        address=data.address,
        aadhaar_url=data.aadhaarUrl,
        pan_url=data.panUrl,
        certificate_url=data.certificateUrl,
        profile_pic_url=data.profilePicUrl,
        skill_category=data.skillCategory,
        sub_category=data.subCategory,
        role_type=data.roleType,
        years=data.years,
        months=data.months,
        agreed=data.agreed,
        skills=[s.model_dump() for s in data.skills],  # store as JSON
        location=data.location.model_dump() if data.location else None,
    )

    db.add(reg)
    await db.commit()
    await db.refresh(reg)
    return reg
