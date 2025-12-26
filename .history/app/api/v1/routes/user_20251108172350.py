from app.models.user_model import RegistrationModel
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

@router.get("/profile/{userId}", status_code=status.HTTP_200_OK)
async def get_user_profile(userId: int = Path(..., description="The ID of the user to retrieve")):
    """
    Retrieve user profile by user ID.
    """
    # Dummy data for demonstration purposes
    dummy_user = {
        "id": userId,
        "name": "John Doe",
        "email": "
