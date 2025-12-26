from app.models.user_model import RegistrationModel
from app.utils.response import custom_response
from fastapi import APIRouter, status


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
