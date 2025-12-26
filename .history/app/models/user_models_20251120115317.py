import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime, timezone


class RegistrationModel(Base):
    __tablename__ = "registrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    phone_number = Column(String)
    name = Column(String, nullable=False)
    address = Column(String)

    aadhaar_url = Column(JSONB, nullable=False)
    pan_url = Column(JSONB, nullable=False)
    certificate_url = Column(JSONB)
    profile_pic_url = Column(String)

    skill_category = Column(String)
    sub_category = Column(String)
    role_type = Column(String)

    years = Column(String)
    months = Column(String)

    agreed = Column(Boolean, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    skills = relationship(
        "Skill", back_populates="registration", cascade="all, delete-orphan"
    )
    location = relationship(
        "Location",
        back_populates="registration",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    registration_id = Column(String, ForeignKey("registrations.id"))

    category = Column(String, nullable=False)
    sub_categories = Column(JSONB, nullable=False)
    industry_type = Column(String, nullable=False)
    tier = Column(String, nullable=False)
    wage = Column(String, nullable=False)
    years = Column(String)
    months = Column(String)

    registration = relationship("Registration", back_populates="skills")


class Location(Base):
    __tablename__ = "locations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    registration_id = Column(String, ForeignKey("registrations.id"))

    latitude = Column(Float)
    longitude = Column(Float)

    registration = relationship("Registration", back_populates="location")
