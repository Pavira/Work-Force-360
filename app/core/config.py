from pydantic import BaseModel
from datetime import timedelta


class Settings(BaseModel):
    PROJECT_NAME: str = "WorkForce 360 API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Enterprise-grade API with versioning, auth, and custom OpenAPI"
    SECRET_KEY: str = "SUPER_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
