from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

# ------------------------
# Submodels
# ------------------------


class SkillModel(BaseModel):
    category: str = Field(..., example="Electrical")
    subCategories: List[str] = Field(..., example=["Wiring", "Maintenance"])
    industryType: str = Field(..., example="Construction")
    tier: str = Field(..., example="Tier 1")
    wage: str = Field(..., example="₹500/day")
    years: str = Field(..., example="3")
    months: str = Field(..., example="4")


class LocationModel(BaseModel):
    latitude: Optional[float] = Field(None, example=13.0827)
    longitude: Optional[float] = Field(None, example=80.2707)


# ------------------------
# Main Registration Model
# ------------------------


class RegistrationModel(BaseModel):
    userId: str = Field(..., example="hdbs73hsb82hss9")
    phoneNumber: Optional[str] = Field(None, example="+919876543210")
    name: str = Field(..., example="Sangeetha S")
    address: Optional[str] = Field(None, example="123, Anna Nagar, Chennai")

    aadhaarUrl: List[HttpUrl] = Field(
        ...,
        example=[
            "https://firebasestorage.googleapis.com/v0/b/app/aadhaar/aadhaar_front.jpg",
            "https://firebasestorage.googleapis.com/v0/b/app/aadhaar/aadhaar_back.jpg",
        ],
    )
    panUrl: List[HttpUrl] = Field(
        ...,
        example=["https://firebasestorage.googleapis.com/v0/b/app/pan/pan_card.jpg"],
    )
    certificateUrl: Optional[List[HttpUrl]] = Field(
        None,
        example=[
            "https://firebasestorage.googleapis.com/v0/b/app/certificates/cert1.jpg"
        ],
    )
    profilePicUrl: Optional[HttpUrl] = Field(
        None,
        example="https://firebasestorage.googleapis.com/v0/b/app/profile/profile_pic.jpg",
    )

    skillCategory: Optional[str] = Field(None, example="Electrical")
    subCategory: Optional[str] = Field(None, example="Wiring")
    roleType: Optional[str] = Field(None, example="Technician")
    years: Optional[str] = Field(None, example="3")
    months: Optional[str] = Field(None, example="4")

    agreed: bool = Field(..., example=True)
    createdAt: datetime = Field(
        default_factory=datetime.now(timezone.utc), example="2025-11-06T06:45:12.000Z"
    )

    skills: List[SkillModel] = Field(default_factory=list)
    location: Optional[LocationModel] = None


# -------------------------------
# Skill Model
# -------------------------------
class ProfileSkillModel(BaseModel):
    category: str = Field(
        ..., description="Main skill category, e.g., Electrical, Plumbing"
    )
    subCategories: List[str] = Field(
        default_factory=list, description="Sub-skills or related categories"
    )
    industryType: str = Field(..., description="Industry type for the skill")
    tier: str = Field(
        ..., description="Skill tier (e.g., beginner, intermediate, expert)"
    )
    wage: str = Field(..., description="Wage or hourly rate")

    class Config:
        schema_extra = {
            "example": {
                "category": "Electrical",
                "subCategories": ["Wiring", "Panel Installation"],
                "industryType": "Construction",
                "tier": "Intermediate",
                "wage": "500",
            }
        }


# -------------------------------
# Bank Details Model
# -------------------------------
class BankDetailsModel(BaseModel):
    accountHolderName: str
    accountNumber: str
    ifscCode: str
    bankName: str
    upiId: str

    class Config:
        schema_extra = {
            "example": {
                "accountHolderName": "Pavi Kumar",
                "accountNumber": "1234567890",
                "ifscCode": "SBIN0001234",
                "bankName": "State Bank of India",
                "upiId": "pavi@upi",
            }
        }


# -------------------------------
# Main Profile Model
# -------------------------------
class ProfileModel(BaseModel):
    userId: str
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    profilePicUrl: Optional[str] = None
    skills: List[ProfileSkillModel] = Field(default_factory=list)
    certificateUrls: List[str] = Field(default_factory=list)
    bankDetails: Optional[BankDetailsModel] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "userId": "UID123456",
                "name": "Pavi",
                "phoneNumber": "+919876543210",
                "profilePicUrl": "https://example.com/profile.jpg",
                "skills": [
                    {
                        "category": "Plumbing",
                        "subCategories": ["Pipe Fitting", "Maintenance"],
                        "industryType": "Construction",
                        "tier": "Expert",
                        "wage": "600",
                    }
                ],
                "certificateUrls": [
                    "https://example.com/cert1.pdf",
                    "https://example.com/cert2.pdf",
                ],
                "bankDetails": {
                    "accountHolderName": "Pavi Kumar",
                    "accountNumber": "1234567890",
                    "ifscCode": "SBIN0001234",
                    "bankName": "SBI",
                    "upiId": "pavi@upi",
                },
                "createdAt": "2025-11-07T10:00:00Z",
                "updatedAt": "2025-11-07T10:00:00Z",
            }
        }
