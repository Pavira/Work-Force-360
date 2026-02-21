from geoalchemy2 import Geography
from sqlalchemy import Column, ForeignKey, String, Boolean, Text, func, text

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime


from app.db.base import Base


class CompanyModel(Base):
    __tablename__ = "companies"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    firebase_uid = Column(String, unique=True, nullable=False, index=True)

    company_name = Column(String, nullable=False)
    industry_id = Column(
        UUID(as_uuid=True),
        ForeignKey("industry_types.id", ondelete="RESTRICT"),
        nullable=False,
    )
    gst_number = Column(String, nullable=True)

    auth_phone = Column(String, nullable=False)

    contact_person_name = Column(String, nullable=True)
    contact_country_code = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, unique=True, nullable=True)

    logo_url = Column(Text, nullable=True)

    status = Column(String, default="draft")
    is_verified = Column(Boolean, default=False)

    is_active = Column(Boolean, server_default=text("true"))

    bank_details = relationship(
        "CompanyBankDetailsModel",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    addresses = relationship(
        "CompanyAddressModel", back_populates="company", cascade="all, delete-orphan"
    )
    documents = relationship(
        "CompanyDocumentModel", back_populates="company", cascade="all, delete-orphan"
    )

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CompanyAddressModel(Base):
    __tablename__ = "company_addresses"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    company_id = Column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True
    )

    address = Column(Text, nullable=False)
    unit_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
    location = Column(Geography("POINT", 4326), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    company = relationship("CompanyModel", back_populates="addresses")


class CompanyDocumentModel(Base):
    __tablename__ = "company_documents"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    company_id = Column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True
    )

    document_type = Column(String, nullable=True, index=True)
    document_url = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    company = relationship("CompanyModel", back_populates="documents")


class CompanyBankDetailsModel(Base):
    __tablename__ = "company_bank_details"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    company_id = Column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True
    )

    bank_name = Column(String, nullable=True)
    account_holder_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    upi_id = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    company = relationship("CompanyModel", back_populates="bank_details")
