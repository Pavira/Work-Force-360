# utils/middlewares.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Request, status
from fastapi.responses import JSONResponse
from firebase_admin import auth


# Exact paths to exclude (e.g., docs, index)
EXCLUDE_PATHS = [
    "/",
    "/openapi.json",
    "/docs",
    "/docs/oauth2-redirect",
    "/redoc",
    "/health",
    "/api/v1/auth/signin",
    "/admin/index.html",
]

EXCLUDE_PREFIXES = [
    "/admin/pages",  # ✅ Signin & other auth pages
    "/admin/assets",  # ✅ JS, CSS
    "/admin/components",  # ✅ HTML components
    "/.well-known",  # ✅ Chrome, browser auto-requests
    "/favicon.ico",  # ✅ Optional
    "/robots.txt",  # ✅ Optional
    "/manifest.json",  # ✅ PWA/Chrome install support
    "/api/v1/appointments/generate_prescription_pdf/",
    "/",
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Exclude open/static paths
        # ✅ Unified skip logic
        if path in EXCLUDE_PATHS or any(
            path.startswith(prefix) for prefix in EXCLUDE_PREFIXES
        ):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.error("🔒 Authorization header missing.")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message": "Authorization header missing",
                    "data": None,
                    "code": status.HTTP_401_UNAUTHORIZED,
                },
            )

        try:
            id_token = auth_header.split("Bearer ")[1]
            decoded_token = auth.verify_id_token(id_token)
            email = decoded_token.get("email")
            logger.info("✅ Decoded email:", email)
            request.state.current_user = decoded_token
            request.state.email = email  # ✅ Attach email to request state
        except Exception as e:
            logger.error(f"🔒 Invalid Token: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message": "Invalid or expired token",
                    "data": None,
                    "code": status.HTTP_401_UNAUTHORIZED,
                },
            )

        response = await call_next(request)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Incoming Request Log
        logger.info(f"📥 {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000  # in ms
        formatted_process_time = "{0:.2f}".format(process_time)

        # Outgoing Response Log
        logger.info(
            f"📤 {response.status_code} {request.url.path} completed in {formatted_process_time}ms"
        )
        return response
