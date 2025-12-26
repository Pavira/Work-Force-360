from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,  # turn on in development
    pool_size=10,
    max_overflow=20,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()



1.studied swagger Openapi, analyse the best response format and Created API response format, 

2.Discuss and explained the api working with sangeetha mam

3. studied about fastapi, explored many different modules like Path, Body, Query parameter, best way to write APIs and compatable with swagger documentation

1. Created backend file structure for workforce app

2. studied git and github refered documentation and some youtube video, how to do version control, how to write proper commit messages and studied about github actions 

3. connected my project with github and vercel and live the api documentation, created a deployement pipline

1. Analyse the requirement and user models provided and created model compatable to fastapi and to match with flutter frontend

2.created user api compatible with swagger documentation, and provide to sangeethaa mam and explained to sangeetha man  about the apis

1. Had a meeting with team and discuss about the project flow

2. Analyse the requirement and profile and work models provided and created model compatable to fastapi and to match with flutter frontend

3. created user api compatible with swagger documentation and live in the vercel, and provide to sangeethaa mam and explained to sangeetha man about the profile apis

1. analyse the requirements of the workforce360, how to structure the backend, compare different technologies flow 

2. Refered many resources and video and created a deployement flow structure, technologies used and pricing

3. Created a summary document of the deployment pipline

4. Did a discussion with akshara man, discussed about aws account, admin panel deployment

5. Did some correction in swartech admin panel, changed github repo, create a vercel account

1. Change the firebase configuration and live the swartech admin panel website in vercel

2. Created AWS account, analyse what services we need in aws, explore the aws console and services, studied 

