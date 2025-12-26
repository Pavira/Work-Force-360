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
    jobId: Optional
