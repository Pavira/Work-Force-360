from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()

# Create an APIRouter and mount it to the main app
router = APIRouter(prefix="/api/v1", tags=["API v1"])


@router.get("/")
async def test_endpoint():
    return {"message": "Hello, World!"}


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
