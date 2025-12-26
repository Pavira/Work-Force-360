from app.schemas.worker_schema import ProfileSchema, WorkerRegistrationSchema
from sqlalchemy import Session
from app.db.session import get_db
from app.services.worker_service import create_worker_service
from app.utils.response import custom_response
from fastapi import APIRouter, status, Path, Depends


router = APIRouter()


@router.post("/create_profile", status_code=status.HTTP_201_CREATED)
async def create_profile(
    worker: WorkerRegistrationSchema, db: Session = Depends(get_db)
):
    """
    Create a new worker registration entry.
    """

    worker_db = await create_worker_service(worker, db)

    return custom_response(
        success=True,
        message=f"Worker {worker_db.name} created successfully.",
        data={"id": worker_db.id, "name": worker_db.name},
        code=status.HTTP_201_CREATED,
    )


# ------------------------# Get User Profile ------------------------
@router.get("/get_profile/{userId}", status_code=status.HTTP_200_OK)
async def get_profile(
    userId: int = Path(..., description="The ID of the user to retrieve")
):
    """
    Retrieve worker profile by user ID.
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


# ------------------------# Update User Profile ------------------------
@router.put("/update_profile", status_code=status.HTTP_200_OK)
async def update_user_profile(
    profile_data: ProfileSchema,
):
    """
    Update user profile by user ID.
    """
    # In a real application, you would update the user profile in the database here.
    updated_profile = profile_data.model_dump(mode="json")
    userId = updated_profile["userId"]

    return custom_response(
        success=True,
        message=f"UserId {userId} profile updated successfully.",
        data=updated_profile,
        code=status.HTTP_200_OK,
    )


# ------------------------# Delete User Profile ------------------------
@router.delete("/delete_profile/{userId}", status_code=status.HTTP_200_OK)
async def delete_user_profile(
    userId: int = Path(..., description="The ID of the user to delete")
):
    """
    Delete user profile by user ID.
    """
    # In a real application, you would delete the user profile from the database here.
    if userId != 1:
        return custom_response(
            success=False,
            message=f"UserId {userId} not found.",
            data={},
            code=status.HTTP_404_NOT_FOUND,
        )

    return custom_response(
        success=True,
        message=f"UserId {userId} profile deleted successfully.",
        data={},
        code=status.HTTP_200_OK,
    )
