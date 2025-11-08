from datetime import datetime, timezone
from typing import List, Optional
from app.utils.response import custom_response
from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi

import uvicorn
from app.core.config import settings
from app.api.v1.routes import auth, user


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    contact={"name": "Pavi", "email": "pavi@company.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "Auth", "description": "User authentication using JWT tokens"},
        {"name": "User", "description": "User management endpoints"},
    ],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
