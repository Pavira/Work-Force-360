from fastapi import FastAPI, APIRouter
import uvicorn

# app = FastAPI()

app = FastAPI(
    title="Inventory Management API",
    description="This API allows you to manage products, view stock, and update details.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
    },
)


@app.get("/", tags=["DEMO API"])
async def test_endpoint():
    """A simple test endpoint that returns a greeting message."""
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
