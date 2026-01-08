from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class CompanyAddressCreateSchema(BaseModel):
    address: str
    unitName: str
    city: str
    state: str
    pincode: str


class CompanyDocumentCreateSchema(BaseModel):
    documentType: Optional[str]
    documentUrl: Optional[str]


class ContactInfoSchema(BaseModel):
    contactPersonName: Optional[str]
    contactPersonPhone: Optional[str]
    contactEmail: Optional[str]


class DocumentInfoSchema(BaseModel):
    logoUrl: Optional[str]
    documents: List[CompanyDocumentCreateSchema]


class CompanyInfoSchema(BaseModel):
    companyName: str
    industryType: str
    gstNo: Optional[str]
    addresses: List[CompanyAddressCreateSchema]
    authPhone: str


class CompanyProfileUpdateSchema(BaseModel):
    companyName: Optional[str]
    industryType: Optional[str]
    gstNo: Optional[str]
    addresses: Optional[List[CompanyAddressCreateSchema]]
    contactInfo: Optional[ContactInfoSchema]
    documentInfo: Optional[DocumentInfoSchema]
