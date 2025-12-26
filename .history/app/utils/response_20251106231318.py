from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone


def custom_response(success: bool, message: str, data=None, code=200):
    response_content = {
        "status_code": code,
        "success": success,
        "message": message,
        "data": data,
        # "code": code,
        "timestamp": datetime.now(timezone.utc),
    }

    return JSONResponse(content=jsonable_encoder(response_content))
