from fastapi import APIRouter, HTTPException, status
from app.core.security import create_access_token
from app.utils.response import custom_response

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(username: str, password: str):
    if username != "admin" or password != "1234":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": username})
    return custom_response(
        success=True,
        message="Login successful",
        data={"access_token": token, "token_type": "bearer"},
        code=status.HTTP_200_OK,
    )
