from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import worker_models, company_model
