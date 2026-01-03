from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import company_models, industry_skill_models

# alembic revision --autogenerate -m "corrected industry and skill model"
# alembic upgrade head
