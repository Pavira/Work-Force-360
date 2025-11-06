from fastapi import FastAPI
import uvicorn

app = FastAPI()

router = app.router(prefix="/api/v1", tags="API v1")


@app.get("/")
def test_endpoint():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
