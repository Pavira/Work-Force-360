import json
import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.utils.logger import logger
from fastapi import HTTPException, status, Header

_db = None


def initialize_firebase():
    """
    Initializes Firebase Admin SDK exactly once per process.
    Safe to call multiple times.
    """
    if firebase_admin._apps:
        return

    firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

    if not firebase_json:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_JSON not set")

    try:
        service_account_info = json.loads(firebase_json)
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)

    except Exception as e:
        raise RuntimeError(f"Firebase initialization failed: {str(e)}")


def verify_firebase_token(token: str) -> dict:
    """
    Verifies Firebase ID token and returns decoded claims.
    """
    try:
        initialize_firebase()  # ✅ CRITICAL FIX
        # return auth.verify_id_token(token)
        decoded_token = auth.verify_id_token(token)
        print("🔥 Firebase  token:", token)
        return decoded_token

    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase token expired",
        )

    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token",
        )

    except Exception as e:
        print("🔥 Firebase auth error:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )


def get_current_user(authorization: str = Header(...)):
    """
    FastAPI dependency to extract and verify Firebase token.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    token = authorization.split(" ")[1]
    return verify_firebase_token(token)


# ----------------------------------Firestore Production Initialization----------------------------------
# Production function for Vercel.
# Set env var: FIREBASE_ADMINSDK_JSON with the full Firebase service account JSON.
def get_firestore():
    global _db

    if _db is not None:
        return _db

    firebase_adminsdk_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if not firebase_adminsdk_json:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing FIREBASE_SERVICE_ACCOUNT_JSON environment variable for production.",
        )

    try:
        firebase_credentials = json.loads(firebase_adminsdk_json)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="FIREBASE_SERVICE_ACCOUNT_JSON is not valid JSON.",
        ) from e

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized (production env)")

        _db = firestore.client()
        return _db
    except Exception as e:
        logger.error(f"Firebase initialization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to initialize Firebase Firestore",
        )


# ----------------------------------Firestore Production Initialization----------------------------------
