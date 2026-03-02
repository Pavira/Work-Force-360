from geoalchemy2 import Geography
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    Integer,
    Boolean,
    Index,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

# Document Types: PAN Card - (PAN), AADHAR - (AC), Certificate - (CR).
# Status: draft, unapproved, approved, rejected, blocked


class WorkerRegistrationModel(Base):
    __tablename__ = "workers"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    firebase_uid = Column(String, unique=True, nullable=False)

    # ---- Personal Info ----
    name = Column(String(255), nullable=False)
    country_code = Column(String(10), nullable=True)
    auth_number = Column(String(32), nullable=True)

    categories = relationship(
        "WorkerSkillCategoryModel",
        back_populates="worker",
        cascade="all, delete-orphan",
    )

    sub_categories = relationship(
        "WorkerSubCategoryModel",
        back_populates="worker",
        cascade="all, delete-orphan",
    )

    # ---- Location ----
    address = Column(Text, nullable=True)
    city = Column(String(120), nullable=True)
    state = Column(String(120), nullable=True)
    pincode = Column(String(20), nullable=True)
    location = Column(Geography("POINT", 4326), nullable=True)

    # ---- Documents ----
    logo_url = Column(Text, nullable=True)
    documents = relationship(
        "WorkerDocumentModel",
        back_populates="worker",
        cascade="all, delete-orphan",
    )
    # ---- Bank Details ----
    bank_details = relationship(
        "WorkerBankDetailsModel",
        back_populates="worker",
        cascade="all, delete-orphan",
    )

    # ---- Status ----
    status = Column(String(50), default="draft", nullable=False)
    is_active = Column(Boolean, server_default=text("true"))
    is_online = Column(Boolean, server_default=text("false"))
    is_available = Column(Boolean, server_default=text("false"))
    current_job_id = Column(UUID(as_uuid=True), nullable=True)

    # ---- Timestamps ----
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class WorkerSkillCategoryModel(Base):
    __tablename__ = "worker_skill_categories"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    worker_id = Column(
        UUID(as_uuid=True), ForeignKey("workers.id"), nullable=False, index=True
    )

    category_skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("category_skills.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ---- Experience ----
    experience_years = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "worker_id",
            "category_skill_id",
            name="uq_worker_category_unique",
        ),
    )
    worker = relationship("WorkerRegistrationModel", back_populates="categories")


class WorkerSubCategoryModel(Base):
    __tablename__ = "worker_skill_subcategories"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    worker_id = Column(
        UUID(as_uuid=True), ForeignKey("workers.id"), nullable=False, index=True
    )

    sub_category_skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sub_category_skills.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "worker_id",
            "sub_category_skill_id",
            name="uq_worker_subcategory_unique",
        ),
    )
    worker = relationship("WorkerRegistrationModel", back_populates="sub_categories")


class WorkerDocumentModel(Base):
    __tablename__ = "worker_documents"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    worker_id = Column(
        UUID(as_uuid=True), ForeignKey("workers.id"), nullable=False, index=True
    )

    document_type = Column(String(120), nullable=True)
    document_url = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    worker = relationship("WorkerRegistrationModel", back_populates="documents")


class WorkerBankDetailsModel(Base):
    __tablename__ = "worker_bank_details"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    worker_id = Column(
        UUID(as_uuid=True), ForeignKey("workers.id"), nullable=False, index=True
    )

    bank_name = Column(String, nullable=True)
    account_holder_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    upi_id = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    worker = relationship("WorkerRegistrationModel", back_populates="bank_details")
