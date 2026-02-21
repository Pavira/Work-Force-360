from typing import List, Optional
from pydantic import BaseModel, Field


# ------------------------Registration Schema ------------------------
class WorkerDocumentCreateSchema(BaseModel):
    documentType: Optional[str] = Field(None, example="AC/PAN/CR")
    documentUrl: Optional[str] = None


class WorkerDocumentInfoSchema(BaseModel):
    logoUrl: Optional[str] = None
    documents: List[WorkerDocumentCreateSchema] = Field(default_factory=list)


class SubCategorySelectionSchema(BaseModel):
    subCategoryIds: Optional[List[str]] = Field(
        default_factory=list,
        examples=[
            "83deb5cd-fc10-4c88-abc0-8d6c2ec85652",
            "d1a2b3c4-e5f6-7890-abcd-1234567890ab",
        ],
    )


class CategorySelectionSchema(BaseModel):
    categoryId: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    experienceYears: Optional[int] = Field(None, example=3)
    subCategoryIds: List[str] = Field(
        default_factory=list,
        examples=[
            "83deb5cd-fc10-4c88-abc0-8d6c2ec85652",
            "d1a2b3c4-e5f6-7890-abcd-1234567890ab",
        ],
    )


# ------------------------
# Main Registration Schema
# ------------------------


class WorkerRegistrationSchema(BaseModel):

    # -------- Personal Info --------
    name: str = Field(..., example="Sangeetha S")
    countryCode: Optional[str] = Field(None, example="+91")
    authNumber: Optional[str] = Field(None, example="9876543210")

    # -------- Skills ---------
    categories: List[CategorySelectionSchema] = Field(default_factory=list)

    # -------- Location ---------
    address: Optional[str] = Field(None, example="123, Anna Nagar, Chennai")
    city: Optional[str] = Field(None, example="Chennai")
    state: Optional[str] = Field(None, example="Tamil Nadu")
    pincode: Optional[str] = Field(None, example="600040")
    latitude: Optional[float] = Field(None, example=13.0827)
    longitude: Optional[float] = Field(None, example=80.2707)

    # --------- Documents ---------
    documentInfo: Optional[WorkerDocumentInfoSchema] = None


class WorkerAddressUpdateSchema(BaseModel):
    address: Optional[str] = Field(None, example="123, Anna Nagar, Chennai")
    city: Optional[str] = Field(None, example="Chennai")
    state: Optional[str] = Field(None, example="Tamil Nadu")
    pincode: Optional[str] = Field(None, example="600040")
    latitude: Optional[float] = Field(None, example=13.0827)
    longitude: Optional[float] = Field(None, example=80.2707)


class WorkerLogoUpdateSchema(BaseModel):
    logoUrl: Optional[str] = None


class WorkerBankDetailsSchema(BaseModel):
    bankName: Optional[str] = None
    accountHolderName: Optional[str] = None
    accountNumber: Optional[str] = None
    ifscCode: Optional[str] = None
    upiId: Optional[str] = None


class WorkerSkillsUpdateSchema(BaseModel):
    categories: List[CategorySelectionSchema] = Field(default_factory=list)
