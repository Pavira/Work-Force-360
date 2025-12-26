from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.worker_models import (
    WorkerRegistrationModel,
)  # Import all models to register them with Base
