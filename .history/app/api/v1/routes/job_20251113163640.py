from app.utils.response import custom_response
from fastapi import APIRouter, status, Path


router = APIRouter()

@router.post("/get_job_postings/{companyId}", status_code=status.HTTP_200_CREATED)
async def get_job_postings(