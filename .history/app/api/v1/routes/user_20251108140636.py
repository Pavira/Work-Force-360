from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "/api/user/registration", status_code=status.HTTP_201_CREATED, tags=["Users"]
)
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
