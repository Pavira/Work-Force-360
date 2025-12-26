from app.utils.response import custom_response
from fastapi import APIRouter, status, Path


router = APIRouter()


# ------------------------# Get job posting ------------------------
@router.post("/get_job_postings/{companyId}", status_code=status.HTTP_200_CREATED)
async def get_job_postings(
    companyId: int = Path(
        ..., description="The ID of the job to retrieve postings for a company"
    )
):
    """
    Retrieve user profile by user ID.
    """
    # Dummy data for demonstration purposes
    dummy_user = {
        "userId": userId,
        "name": "Sangeetha S",
        "phoneNumber": "+919876543210",
        "address": "123, Anna Nagar, Chennai",
        "aadhaarUrl": [
            "https://firebasestorage.googleapis.com/v0/b/app/aadhaar/aadhaar_front.jpg",
            "https://firebasestorage.googleapis.com/v0/b/app/aadhaar/aadhaar_back.jpg",
        ],
        "panUrl": ["https://firebasestorage.googleapis.com/v0/b/app/pan/pan_card.jpg"],
        "certificateUrl": [
            "https://firebasestorage.googleapis.com/v0/b/app/certificates/cert1.jpg"
        ],
        "profilePicUrl": "https://firebasestorage.googleapis.com/v0/b/app/profile/profile_pic.jpg",
        "skillCategory": "Electrical",
        "subCategory": "Wiring",
        "roleType": "Technician",
        "years": "3",
        "months": "4",
        "agreed": True,
    }
    if userId != 1:
        return custom_response(
            success=False,
            message=f"UserId {userId} not found.",
            data={},
            code=status.HTTP_404_NOT_FOUND,
        )
    return custom_response(
        success=True,
        message=f"UserId {userId} profile retrieved successfully.",
        data=dummy_user,
        code=status.HTTP_200_OK,
    )
