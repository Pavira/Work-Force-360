from app.models.user_model import ProfileModel, RegistrationModel
from app.utils.response import custom_response
from fastapi import APIRouter, status, Path


router = APIRouter()


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration(user: RegistrationModel):
    """
    Create a new worker registration entry.
    """

    return custom_response(
        success=True,
        message=f"User {user.name} created successfully.",
        data=user.model_dump(mode="json"),
        code=status.HTTP_201_CREATED,
    )


# ------------------------# Get User Profile ------------------------
@router.get("/get_profile/{userId}", status_code=status.HTTP_200_OK)
async def get_user_profile(
    userId: int = Path(..., description="The ID of the user to retrieve")
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


# ------------------------# Update User Profile ------------------------
@router.put("/update_profile", status_code=status.HTTP_200_OK)
async def update_user_profile(
    profile_data: ProfileModel,
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
