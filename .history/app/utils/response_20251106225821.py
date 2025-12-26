from fastapi.responses import JSONResponse
from datetime import datetime


def custom_response(success: bool, message: str, data=None, code=200):
    return JSONResponse(
        status_code=code,
        content={
            "success": success,
            "message": message,
            "data": data,
            "code": code,
            "timestamp": datetime.now(datetime.timezone.utc),
        },
    )
