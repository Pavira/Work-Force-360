from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ------------------------
# Submodels
# ------------------------


class LocationModel(BaseModel):
    latitude: Optional[float] = Field(None, example=13.0827)
    longitude: Optional[float] = Field(None, example=80.2707)
    address: Optional[str] = Field(None, example="123, Anna Nagar, Chennai, Tamil Nadu")


class ContactModel(BaseModel):
    name: Optional[str] = Field(None, example="Suresh Kumar")
    phoneNumber: Optional[str] = Field(None, example="+919876543210")
    email: Optional[str] = Field(None, example="suresh@example.com")


# ------------------------
# Main Model
# ------------------------


class JobPostingModel(BaseModel):
    # Basic info
    jobId: Optional[str] = Field(None, example="JOB123456")
    createdBy: str = Field(..., example="EMPLOYER001")
    skillCategory: Optional[str] = Field(None, example="Electrical")
    subCategory: Optional[str] = Field(None, example="Wiring")
    industryType: Optional[str] = Field(None, example="Construction")
    tier: Optional[int] = Field(None, example=1)
    description: Optional[str] = Field(
        None, example="Need an experienced electrician for 3 days site work"
    )

    # Timing
    startDate: Optional[str] = Field(None, example="2025-11-10")
    startTime: Optional[str] = Field(None, example="09:00 AM")
    endDate: Optional[str] = Field(None, example="2025-11-13")
    endTime: Optional[str] = Field(None, example="05:00 PM")
    duration: Optional[str] = Field(None, example="3")
    durationType: Optional[str] = Field(None, example="Days")
    shift: Optional[str] = Field(None, example="Morning")

    # Location
    location: Optional[LocationModel] = None

    # Payment
    wageType: str = Field(..., example="Daily")  # e.g., Hourly, Daily, Monthly
    wage: int = Field(..., example=600)
    expectedTotal: int = Field(..., example=1800)
    paymentTerms: str = Field(..., example="Full payment after job completion")

    # Workforce
    workers: int = Field(..., example=5)
    experienceRequired: Optional[str] = Field(
        None, example="2+ years in wiring and maintenance"
    )

    # Job Rules
    uniformRequired: bool = Field(..., example=True)
    uniformDetails: Optional[str] = Field(
        None, example="Blue overalls and safety shoes mandatory"
    )
    toolProvided: bool = Field(..., example=False)
    toolDetails: Optional[str] = Field(
        None, example="Workers should bring their own tools"
    )
    languagePreference: Optional[str] = Field(None, example="Tamil, English")
    specialInstructions: Optional[str] = Field(
        None, example="Report at main gate by 8:45 AM"
    )

    # Contact
    contact: ContactModel

    # System fields
    status: str = Field(..., example="Open")  # e.g., Open, Assigned, Closed
    createdAt: Optional[datetime] = Field(
        default_factory=datetime.utcnow, example="2025-11-06T06:45:12.000Z"
    )


from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


# ------------------------
# Submodel
# ------------------------


class WorkerModel(BaseModel):
    workerId: str = Field(..., example="W123456")
    name: str = Field(..., example="Sangeetha S")
    phone: str = Field(..., example="+919876543210")
    photoUrl: Optional[HttpUrl] = Field(
        None,
        example="https://firebasestorage.googleapis.com/v0/b/app/profile/worker_photo.jpg",
    )
    rating: Optional[float] = Field(None, example=4.7)


# ------------------------
# Main Job Detail Model
# ------------------------


class JobDetailModel(BaseModel):
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

    assignedWorker: Optional[WorkerModel] = None
