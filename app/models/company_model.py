from sqlalchemy import Column, ForeignKey, String, Boolean, Text, func

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy import DateTime


from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    firebase_uid = Column(String, unique=True, nullable=False, index=True)

    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    gst_number = Column(String, nullable=True)

    contact_person_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    logo_url = Column(Text, nullable=True)

    status = Column(String, default="pending")
    is_verified = Column(Boolean, default=False)

    addresses = relationship(
        "CompanyAddress", back_populates="company", cascade="all, delete-orphan"
    )
    documents = relationship(
        "CompanyDocument", back_populates="company", cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class CompanyAddress(Base):
    __tablename__ = "company_addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True
    )

    address = Column(Text, nullable=False)
    unit_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    company = relationship("Company", back_populates="addresses")


class CompanyDocument(Base):
    __tablename__ = "company_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_id = Column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True
    )

    document_type = Column(String, nullable=False, index=True)
    document_url = Column(Text, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    company = relationship("Company", back_populates="documents")
