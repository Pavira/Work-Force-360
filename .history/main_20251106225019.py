from datetime import datetime
from typing import Optional
from app.utils.response import custom_response
from fastapi import FastAPI, APIRouter, status, Body
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


@app.post("/api/user/registration", status_code=status.HTTP_201_CREATED, tags=["User"])
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
