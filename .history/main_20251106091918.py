from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()


@app.get("/", tags=["DEMO API"])
async def test_endpoint():
    """A simple test endpoint that returns a greeting message."""
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
