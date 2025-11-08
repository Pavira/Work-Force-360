from datetime import datetime
from typing import List, Optional
from app.utils.response import custom_response
from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, HttpUrl
import uvicorn
from app.core.config import settings
from app.api.v1.routes import auth


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact={"name": "Pavi", "email": "pavi@company.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "Auth", "description": "User authentication using JWT tokens"},
        {"name": "Users", "description": "User management endpoints"},
    ],
)

app.include_router(auth.router, prefix="/api/v1")


# Custom OpenAPI Branding
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title=f"{settings.PROJECT_NAME} (Customized Docs)",
#         version=settings.VERSION,
#         description=settings.DESCRIPTION,
#         routes=app.routes,
#     )
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi


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
        default_factory=datetime.utcnow, example="2025-11-06T06:45:12.000Z"
    )

    skills: List[SkillModel] = Field(default_factory=list)
    location: Optional[LocationModel] = None


@app.post("/api/user/registration", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def registration(user: RegistrationModel):
    """
    Create a new worker registration entry.
    """

    return custom_response(
        success=True,
        message=f"User {user.name} created successfully.",
        data=user.model_dump(mode="json"),
        code=status.HTTP_201_CREATED,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
