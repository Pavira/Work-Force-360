from fastapi import FastAPI, APIRouter, status
import uvicorn

# app = FastAPI()

app = FastAPI(
    title="Inventory Management API",
    description="This API allows you to manage products, view stock, and update details.",
    version="1.2.0",
    # contact={
    #     "name": "API Support",
    #     "email": "support@example.com",
    # },
    # license_info={
    #     "name": "MIT License",
    # },
    # openapi_url=None,  # Disable OpenAPI documentation generation
    # docs_url=None,  # Disable Swagger UI
)


@app.get("/", tags=["DEMO API"])
async def test_endpoint():
    """A simple test endpoint that returns a greeting message."""
    return {"message": "Hello, World!"}


@app.psot("/api/user/registration", status_code=status.HTTP_201_CREATED, tags=["User"])
async def registration():
    """A API endpoint for user registration."""
    return {
        "success": True,
        "message": "Hello, World!",
        "data": "[1,2,3,4,5,6,7,8,9,10]",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
