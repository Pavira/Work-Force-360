from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = (
    settings.DATABASE_URL
)  # Example: postgresql+psycopg2://user:pass@ServerEndpoint:5432/dbname

# Sync engine
engine = create_engine(
    DATABASE_URL,
    # echo=True,  # Enable SQL query logs during development
    # echo="debug",  # Enable detailed SQL query logs
    future=True,  # Enables SQLAlchemy 2.0 API behavior
)

# Session factory (sync)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()  # ✅ THIS WAS MISSING
    except:
        db.rollback()  # ✅ Safety
        raise
    finally:
        db.close()
