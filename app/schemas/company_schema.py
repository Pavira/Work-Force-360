from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional


class CompanyAddressCreateSchema(BaseModel):
    address: str
    unitName: str
    city: str
    state: str
    pincode: str


class CompanyDocumentCreateSchema(BaseModel):
    documentType: Optional[str] = None
    documentUrl: Optional[str] = None


class ContactInfoSchema(BaseModel):
    contactPersonName: Optional[str] = None
    contactPersonPhone: Optional[str] = None
    contactEmail: Optional[str] = None


class DocumentInfoSchema(BaseModel):
    logoUrl: Optional[str] = None
    documents: List[CompanyDocumentCreateSchema] = Field(default_factory=list)


class CompanyInfoSchema(BaseModel):
    companyName: str
    industryName: str
    industryId: UUID
    gstNo: Optional[str] = None
    addresses: List[CompanyAddressCreateSchema]
    authPhone: str


class CompanyProfileUpdateSchema(BaseModel):
    companyName: Optional[str] = None
    industryType: Optional[str] = None
    gstNo: Optional[str] = None
    addresses: Optional[List[CompanyAddressCreateSchema]] = None
    contactInfo: Optional[ContactInfoSchema] = None
    documentInfo: Optional[DocumentInfoSchema] = None

    class Config:
        extra = "forbid"  # Forbid extra fields not defined in the schema


class UploadUrlRequest(BaseModel):
    file_type: str


class CompanyProfileDetailsSchema(BaseModel):
    companyName: str
    industryName: str
    industryId: UUID
    gstNo: Optional[str] = None


class CompanyBankDetailsSchema(BaseModel):
    bankName: Optional[str] = None
    accountHolderName: Optional[str] = None
    accountNumber: Optional[str] = None
    ifscCode: Optional[str] = None
    upiId: Optional[str] = None
