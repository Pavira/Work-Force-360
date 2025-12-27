from datetime import datetime, timezone
from typing import List, Optional
from app.core import limiter
from app.utils.response import custom_response
from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi

import uvicorn
from app.core.config import settings
from app.api.v1.routes import auth, company, job, worker

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    # description=settings.DESCRIPTION,
    # contact={"name": "Pavi", "email": "pavi@company.com"},
    # license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "Auth", "description": "User authentication using JWT tokens"},
        {"name": "Worker", "description": "Worker management endpoints"},
        {"name": "Job", "description": "Job posting and management endpoints"},
    ],
)

# Include Routers
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
# app.include_router(worker.router, prefix="/api/v1/worker", tags=["Worker"])
# app.include_router(job.router, prefix="/api/v1/job", tags=["Job"])
app.include_router(company.router, prefix="/api/v1/company", tags=["Company"])

# Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Custom OpenAPI Branding
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=f"{settings.PROJECT_NAME} (Customized Docs)",
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return custom_response(
        success=True,
        message="API is up and running.",
        data={"version": settings.VERSION},
        code=status.HTTP_200_OK,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
