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
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class WorkerRegistrationModel(Base):
    __tablename__ = "workers"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    firebase_uid = Column(String, unique=True, nullable=False, index=True)

    # ---- Personal Info ----
    name = Column(String(255), nullable=False)
    auth_number = Column(String(32), nullable=True, index=True)

    # ---- Skills ----
    category_id = Column(UUID(as_uuid=True), nullable=True)
    category_name = Column(String(150), nullable=True)

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

    # ---- Experience ----
    years = Column(Integer, nullable=True)

    # ---- Documents ----
    logo_url = Column(Text, nullable=True)
    documents = relationship(
        "WorkerDocumentModel",
        back_populates="worker",
        cascade="all, delete-orphan",
    )

    # ---- Status ----
    status = Column(String(50), default="draft", nullable=False)
    is_active = Column(Boolean, server_default=text("true"))

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


class WorkerSubCategoryModel(Base):
    __tablename__ = "worker_skill_selections"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    worker_id = Column(
        UUID(as_uuid=True), ForeignKey("workers.id"), nullable=False, index=True
    )

    sub_category_id = Column(UUID(as_uuid=True), nullable=False)
    sub_category_name = Column(String(150), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
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

    document_type = Column(String(120), nullable=True, index=True)
    document_url = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    worker = relationship("WorkerRegistrationModel", back_populates="documents")
