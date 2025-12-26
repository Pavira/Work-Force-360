from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


# ------------------------Registration Schema ------------------------
# ------------------------
# SubSchemas
# ------------------------


class SkillSchema(BaseModel):
    category: str = Field(..., example="Electrical")
    subCategories: List[str] = Field(..., example=["Wiring", "Maintenance"])
    industryType: str = Field(..., example="Construction")
    tier: str = Field(..., example="Tier 1")
    wage: str = Field(..., example="₹500/day")
    years: str = Field(..., example="3")
    months: str = Field(..., example="4")


class LocationSchema(BaseModel):
    latitude: Optional[float] = Field(None, example=13.0827)
    longitude: Optional[float] = Field(None, example=80.2707)


# ------------------------
# Main Registration Schema
# ------------------------


class RegistrationSchema(BaseModel):
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

    skills: List[SkillSchema] = Field(default_factory=list)
    location: Optional[LocationSchema] = None


# -------------------------------# Profile Schemas #------------------------


# -------------------------------
# Skill Schema
# -------------------------------
class ProfileSkillSchema(BaseModel):
    category: str = Field(
        ...,
        description="Main skill category, e.g., Electrical, Plumbing",
        example="Electrical",
    )
    subCategories: List[str] = Field(
        default_factory=list,
        description="Sub-skills or related categories",
        example=["Wiring", "Maintenance", "Panel Setup"],
    )
    industryType: str = Field(
        ..., description="Industry type for the skill", example="Construction"
    )
    tier: str = Field(
        ...,
        description="Skill tier (e.g., beginner, intermediate, expert)",
        example="Intermediate",
    )
    wage: str = Field(..., description="Wage or hourly rate", example="₹500/day")


# -------------------------------
# Bank Details Schema
# -------------------------------
class BankDetailsSchema(BaseModel):
    accountHolderName: str = Field(
        ..., description="Full name of the account holder", example="Ravi Kumar"
    )
    accountNumber: str = Field(
        ..., description="Bank account number", example="123456789012"
    )
    ifscCode: str = Field(
        ..., description="Bank IFSC code for transfer", example="SBIN0005678"
    )
    bankName: str = Field(
        ..., description="Name of the bank", example="State Bank of India"
    )
    upiId: str = Field(
        ..., description="Linked UPI ID for payments", example="ravi@sbi"
    )


# -------------------------------
# Main Profile Schema
# -------------------------------
class ProfileSchema(BaseModel):
    userId: str = Field(
        ...,
        description="Unique user identifier (Firebase UID or UUID)",
        example="UID_1234567890",
    )
    name: Optional[str] = Field(
        None, description="Full name of the user", example="Ravi Kumar"
    )
    phoneNumber: Optional[str] = Field(
        None, description="Registered mobile number", example="+919876543210"
    )
    profilePicUrl: Optional[str] = Field(
        None,
        description="Profile picture download URL",
        example="https://storage.googleapis.com/app/profilepics/ravi.jpg",
    )
    skills: List[ProfileSkillSchema] = Field(
        default_factory=list, description="List of user skills with subcategories"
    )
    certificateUrls: List[str] = Field(
        default_factory=list,
        description="List of certificate image URLs",
        example=[
            "https://storage.googleapis.com/app/certificates/electrical1.jpg",
            "https://storage.googleapis.com/app/certificates/electrical2.jpg",
        ],
    )
    bankDetails: Optional[BankDetailsSchema] = Field(
        None, description="Bank details for payments or salary transfers"
    )
    createdAt: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC)",
        example="2025-11-07T10:30:00Z",
    )
    updatedAt: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Last updated timestamp (UTC)",
        example="2025-11-07T12:00:00Z",
    )
