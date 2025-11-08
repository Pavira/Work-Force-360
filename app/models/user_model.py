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
