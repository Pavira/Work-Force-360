from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    future=True,  # Enables SQLAlchemy 2.0 style behavior even if using older versions.
    echo=False,  # turn on in development
    pool_size=10,  # Maintain a pool of 10 connections.
    max_overflow=20,  # Allows 20 extra temporary connections when load spikes.
)

session = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with session() as session:
        try:
            yield session
        finally:
            await session.close()
