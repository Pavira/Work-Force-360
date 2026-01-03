from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class CompanyAddressCreateSchema(BaseModel):
    address: str
    unitName: Optional[str]
    city: str
    state: str
    pincode: str


class CompanyDocumentCreateSchema(BaseModel):
    documentType: str
    documentUrl: str


class CompanyRegistrationSchema(BaseModel):
    companyName: str
    industry: str
    gst: Optional[str]

    contactPersonName: str
    phone: str
    email: str
    phone: str

    logoUrl: Optional[str]

    addresses: List[CompanyAddressCreateSchema]
    documents: List[CompanyDocumentCreateSchema]
