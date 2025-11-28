import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Float,
    Integer,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime, timezone


class WorkerRegistrationModel(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20))
    name = Column(String(255), nullable=False)
    address = Column(String)

    aadhaar_url = Column(JSONB, nullable=False)
    pan_url = Column(JSONB, nullable=False)
    certificate_url = Column(JSONB, server_default="[]")
    profile_pic_url = Column(String)

    skill_category = Column(String)
    sub_category = Column(String)
    role_type = Column(String)
    years = Column(String)
    months = Column(String)

    agreed = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    skills = Column(JSONB, server_default="[]")
    location = Column(JSONB)
