from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = (
    settings.DATABASE_URL
)  # Example: postgresql+psycopg2://user:pass@localhost:5432/dbname

# Sync engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Enable SQL query logs during development
    future=True,  # Enables SQLAlchemy 2.0 API behavior
)

# Session factory (sync)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for table inheritance
Base = declarative_base()


def get_db():
    """
    Database dependency for Sync FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
