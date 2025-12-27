from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class CompanyAddressCreate(BaseModel):
    address: str
    unitName: Optional[str]
    city: str
    state: str
    pincode: str


class CompanyDocumentCreate(BaseModel):
    documentType: str
    documentUrl: str


class CompanyCreate(BaseModel):
    companyName: str
    industry: str
    gst: Optional[str]

    contactPersonName: str
    email: str
    phone: str

    logoUrl: Optional[str]

    addresses: List[CompanyAddressCreate]
    documents: List[CompanyDocumentCreate]
