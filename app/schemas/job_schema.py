from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import date, datetime, time


# ------------------------
# Job Post Schema
# ------------------------


class JobPostingSchema(BaseModel):
    # Basic info
    skillCategoryId: Optional[str] = Field(
        None, example="cd973909-d6e2-4fa7-be1a-3f8f875220f0"
    )
    subCategoryId: Optional[str] = Field(
        None, example="83deb5cd-fc10-4c88-abc0-8d6c2ec85652"
    )
    industryTypeId: Optional[str] = Field(
        None,
        example="13c43402-faa9-4f42-b295-3e26a3f8f12b",
    )
    tier: Optional[int] = Field(None, example=1)
    description: Optional[str] = Field(
        None, example="Need an experienced electrician for 3 days site work"
    )

    # Location
    latitude: Optional[float] = Field(None, example=13.0827)
    longitude: Optional[float] = Field(None, example=80.2707)
    workAddress: Optional[str] = Field(
        None, example="123, Anna Nagar, Chennai, Tamil Nadu"
    )
    nearbyLandmark: Optional[str] = Field(None, example="Near Anna Nagar Tower Park")

    # -------- Timing (Timezone Aware) --------
    scheduledStartDateTime: Optional[datetime] = Field(
        None, example="2026-02-15T09:00:00+05:30"
    )
    scheduledEndDateTime: Optional[datetime] = Field(
        None, example="2026-02-15T18:00:00+05:30"
    )
    scheduledDuration: str = Field(..., example="3")
    durationType: Optional[str] = Field(None, example="hours/days")
    shift: Optional[str] = Field(None, example="Day/Night/Rotational")

    # Workforce
    workers: int = Field(..., example=5)
    experienceRequired: Optional[int] = Field(None, example="2")

    # Payment
    wage: int = Field(..., example=600)
    expectedTotal: int = Field(..., example=1800)

    # Contact
    name: Optional[str] = Field(None, example="Suresh Kumar")
    countryCode: Optional[str] = Field(None, example="+91")
    phoneNumber: Optional[str] = Field(None, example="+919876543210")
    email: Optional[str] = Field(None, example="suresh@example.com")

    # Job Rules
    languagePreference: Optional[str] = Field(None, example="Tamil, English")
    toolProvided: bool = Field(None, example=False)
    toolDetails: Optional[str] = Field(
        None, example="Company will not provide any tools"
    )
    specialInstructions: Optional[str] = Field(
        None, example="Report at main gate by 8:45 AM"
    )
