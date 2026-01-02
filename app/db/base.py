from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import company_models, worker_models, industry_skill_models
