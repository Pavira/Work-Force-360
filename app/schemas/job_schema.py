from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import date, datetime, time


# ------------------------
# Job Post Schema
# ------------------------


class JobPostingSchema(BaseModel):
    # Basic info
    skillCategoryId: Optional[str] = Field(None, example="SC123456")
    subCategoryId: Optional[str] = Field(None, example="SUBSC123456")
    industryTypeId: Optional[str] = Field(None, example="IT123456")
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
    scheduledStartDateTime: datetime = Field(..., example="2026-02-15T09:00:00+05:30")
    scheduledEndDateTime: datetime = Field(..., example="2026-02-15T18:00:00+05:30")
    scheduledDuration: Optional[str] = Field(None, example="3")
    durationType: Optional[str] = Field(None, example="hours/days")
    shift: Optional[str] = Field(None, example="Day/Night/Rotational")

    # Workforce
    workers: int = Field(..., example=5)
    experienceRequired: Optional[str] = Field(None, example="2+ years")

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
    toolProvided: bool = Field(..., example=False)
    toolDetails: Optional[str] = Field(
        None, example="Company will not provide any tools"
    )
    specialInstructions: Optional[str] = Field(
        None, example="Report at main gate by 8:45 AM"
    )


# ------------------------
# SubSchema
# ------------------------


class WorkerSchema(BaseModel):
    workerId: str = Field(..., example="W123456")
    name: str = Field(..., example="Sangeetha S")
    phone: str = Field(..., example="+919876543210")
    photoUrl: Optional[HttpUrl] = Field(
        None,
        example="https://firebasestorage.googleapis.com/v0/b/app/profile/worker_photo.jpg",
    )
    rating: Optional[float] = Field(None, example=4.7)


# ------------------------
# Main Job Detail Schema
# ------------------------


class JobDetailSchema(BaseModel):
    jobId: str = Field(..., example="JOB98765")
    role: str = Field(..., example="Electrician")
    companyName: str = Field(..., example="ABC Infra Pvt Ltd")
    wage: float = Field(..., example=650.0)
    status: str = Field(
        ..., example="Ongoing"
    )  # e.g., Open, Ongoing, Completed, Cancelled

    startDate: str = Field(..., example="2025-11-10")
    startTime: str = Field(..., example="09:00 AM")
    endDate: Optional[str] = Field(None, example="2025-11-12")
    endTime: Optional[str] = Field(None, example="06:00 PM")

    assignedWorker: Optional[WorkerSchema] = None


# ------------------------ Job Post Schema ------------------------
class JobPostSchema(BaseModel):
    # Basic Info
    id: str = Field(..., example="JOB123456")
    title: Optional[str] = Field(None, example="Electrical Maintenance Work")
    subCategory: Optional[str] = Field(None, example="Wiring")
    companyId: Optional[str] = Field(None, example="COMP456789")
    companyName: Optional[str] = Field(None, example="ABC Infra Pvt Ltd")
    companyLogoUrl: Optional[HttpUrl] = Field(
        None,
        example="https://firebasestorage.googleapis.com/v0/b/app/logo/company_logo.jpg",
    )
    createdBy: Optional[str] = Field(None, example="EMP12345")

    # Contact Info
    contactName: Optional[str] = Field(None, example="Suresh Kumar")
    contactPhone: Optional[str] = Field(None, example="+919876543210")

    # Job Details
    status: Optional[str] = Field(
        None, example="Open"
    )  # e.g., Open, Assigned, Completed, Cancelled
    tier: Optional[int] = Field(None, example=2)
    wage: Optional[float] = Field(None, example=650.0)
    startDate: Optional[str] = Field(None, example="2025-11-10")
    startTime: Optional[str] = Field(None, example="09:00 AM")
    endDate: Optional[str] = Field(None, example="2025-11-12")
    endTime: Optional[str] = Field(None, example="06:00 PM")
    isNext: Optional[bool] = Field(None, example=False)

    # Ratings
    ratingByCompany: Optional[float] = Field(None, example=4.8)
    ratingByWorker: Optional[float] = Field(None, example=4.5)

    # Firestore Timestamp Equivalents
    createdAt: Optional[datetime] = Field(None, example="2025-11-06T06:45:12.000Z")
    startTimestamp: Optional[datetime] = Field(None, example="2025-11-10T09:00:00.000Z")
    endTimestamp: Optional[datetime] = Field(None, example="2025-11-12T18:00:00.000Z")
    pendingSince: Optional[datetime] = Field(None, example="2025-11-06T06:45:12.000Z")
    pendingExpiresAt: Optional[datetime] = Field(
        None, example="2025-11-07T06:45:12.000Z"
    )
    confirmedAt: Optional[datetime] = Field(None, example="2025-11-06T10:00:00.000Z")
    rejectExpiresAt: Optional[datetime] = Field(
        None, example="2025-11-07T10:00:00.000Z"
    )
    startedAt: Optional[datetime] = Field(None, example="2025-11-10T09:00:00.000Z")
    completedAt: Optional[datetime] = Field(None, example="2025-11-12T18:00:00.000Z")
    cancelledAt: Optional[datetime] = Field(None, example="2025-11-09T20:00:00.000Z")

    # System / Meta
    cancelledBy: Optional[str] = Field(None, example="Worker123")
    autoAssigned: Optional[bool] = Field(None, example=True)
    penalty: Optional[int] = Field(None, example=200)
