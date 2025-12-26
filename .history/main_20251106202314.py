from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Body, status
from pydantic import BaseModel, Field, HttpUrl
import uvicorn

app = FastAPI(
    title="Work Force 360",
    version="1.0.0",
    description="Demo API for Swagger examples with Pydantic and FastAPI.",
)


class RegistrationModel(BaseModel):
    userId: str = Field(..., example="hdbs73hsb82hss9")
    phoneNumber: Optional[str] = Field(None, example="+919876543210")
    name: str = Field(
        ..., description="Full name of the customer", example="Sangeetha S"
    )
    aadhaarUrl: Optional[HttpUrl] = Field(
        None,
        example="https://firebasestorage.googleapis.com/v0/b/app/aadhaar/aadhaar_front.jpg",
    )
    panUrl: Optional[HttpUrl] = Field(
        None, example="https://firebasestorage.googleapis.com/v0/b/app/pan/pan_card.jpg"
    )
    certificateUrl: Optional[HttpUrl] = Field(
        None,
        example="https://firebasestorage.googleapis.com/v0/b/app/certificates/cert1.jpg",
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
    createdAt: Optional[datetime] = Field(None, example="2025-11-06T06:45:12.000Z")


@app.post("/api/user/test", status_code=status.HTTP_201_CREATED, tags=["User"])
async def registration(
    user: RegistrationModel = Body(
        ...,
        examples={
            "normal": {
                "summary": "Normal customer",
                "description": "A regular active customer",
                "value": {
                    "userId": "hdbs73hsb82hss9",
                    "phoneNumber": "+919876543210",
                    "name": "Sangeetha S",
                    "aadhaarUrl": "https://firebasestorage.googleapis.com/v0/b/app/aadhaar/aadhaar_front.jpg",
                    "panUrl": "https://firebasestorage.googleapis.com/v0/b/app/pan/pan_card.jpg",
                    "certificateUrl": "https://firebasestorage.googleapis.com/v0/b/app/certificates/cert1.jpg",
                    "profilePicUrl": "https://firebasestorage.googleapis.com/v0/b/app/profile/profile_pic.jpg",
                    "skillCategory": "Electrical",
                    "subCategory": "Wiring",
                    "roleType": "Technician",
                    "years": "3",
                    "months": "4",
                    "agreed": True,
                    "createdAt": "2025-11-06T06:45:12.000Z",
                },
            },
            "inactive": {
                "summary": "Inactive customer",
                "description": "A user who has not agreed to terms",
                "value": {
                    "userId": "123456",
                    "phoneNumber": "+8103456987",
                    "name": "Pavithiran",
                    "aadhaarUrl": "https://firebasestorage.googleapis.com/v0/b/app/aadhaar/aadhaar_front.jpg",
                    "panUrl": "https://firebasestorage.googleapis.com/v0/b/app/pan/pan_card.jpg",
                    "certificateUrl": "https://firebasestorage.googleapis.com/v0/b/app/certificates/cert1.jpg",
                    "profilePicUrl": "https://firebasestorage.googleapis.com/v0/b/app/profile/profile_pic.jpg",
                    "skillCategory": "Electrical",
                    "subCategory": "Wiring",
                    "roleType": "Technician",
                    "years": "3",
                    "months": "4",
                    "agreed": False,
                    "createdAt": "2025-11-06T06:45:12.000Z",
                },
            },
        },
    )
):
    """
    Create a new worker registration entry.
    """
    return {
        "success": True,
        "message": f"User {user.name} registered successfully.",
        "data": user,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
