from typing import List, Optional
from pydantic import BaseModel, Field


# ------------------------Registration Schema ------------------------
class WorkerDocumentCreateSchema(BaseModel):
    documentType: Optional[str] = None
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
    subCategoryNames: Optional[List[str]] = Field(
        default_factory=list, examples=["Wiring", "Appliance Repair"]
    )


# ------------------------
# Main Registration Schema
# ------------------------


class WorkerRegistrationSchema(BaseModel):

    # -------- Personal Info --------
    name: str = Field(..., example="Sangeetha S")
    authNumber: Optional[str] = Field(None, example="+919876543210")

    # -------- Skills ---------
    categoryId: Optional[str] = Field(
        None, example="cd973909-d6e2-4fa7-be1a-3f8f875220f0"
    )
    categoryName: Optional[str] = Field(None, example="Electrical")
    subCategory: Optional[SubCategorySelectionSchema] = None

    # -------- Location ---------
    address: Optional[str] = Field(None, example="123, Anna Nagar, Chennai")
    city: Optional[str] = Field(None, example="Chennai")
    state: Optional[str] = Field(None, example="Tamil Nadu")
    pincode: Optional[str] = Field(None, example="600040")
    latitude: Optional[float] = Field(None, example=13.0827)
    longitude: Optional[float] = Field(None, example=80.2707)

    # --------- Experience ---------
    years: Optional[int] = Field(None, example=3)

    # --------- Documents ---------
    documentInfo: Optional[WorkerDocumentInfoSchema] = None
