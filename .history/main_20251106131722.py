from datetime import datetime
from typing import Optional
from fastapi import FastAPI, APIRouter, status
from pydantic import BaseModel, Field, HttpUrl
import uvicorn

# app = FastAPI()

app = FastAPI(
    title="Work Force 360",
    description="",
    version="1.0.0",
    # contact={
    #     "name": "API Support",
    #     "email": "support@example.com",
    # },
    # license_info={
    #     "name": "MIT License",
    # },
    # openapi_url=None,  # Disable OpenAPI documentation generation
    # docs_url=None,  # Disable Swagger UI
)


# @app.get("/", tags=["DEMO API"])
# async def test_endpoint():
#     """A simple test endpoint that returns a greeting message."""
#     return {"message": "Hello, World!"}


class RegistrationModel(BaseModel):
    userId: str = Field(..., example="hdbs73hsb82hss9")
    phoneNumber: Optional[str] = Field(None, example="+919876543210")
    name: str = Field(..., example="Sangeetha S")
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


@app.post("/api/user/registration", status_code=status.HTTP_201_CREATED, tags=["User"])
async def registration(user: RegistrationModel):
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
