from fastapi import APIRouter, HTTPException
from app.core.firebase_auth import get_firestore
from pydantic import BaseModel

router = APIRouter()


class PinVerifyRequest(BaseModel):
    pin: str


class PinChangeRequest(BaseModel):
    current_pin: str
    new_pin: str


@router.post("/verify-pin")
def verify_pin(payload: PinVerifyRequest):
    db = get_firestore()
    doc = db.collection("Login").document("pin").get()

    if not doc.exists:
        raise HTTPException(status_code=500, detail="PIN not configured")

    saved_pin = doc.to_dict().get("login_pin")

    if payload.pin != saved_pin:
        raise HTTPException(status_code=401, detail="Invalid PIN")

    return {"success": True, "message": "PIN verified successfully"}


@router.post("/change-pin")
def change_pin(payload: PinChangeRequest):
    db = get_firestore()

    # First verify current PIN
    doc = db.collection("Login").document("pin").get()

    if not doc.exists:
        raise HTTPException(status_code=500, detail="PIN not configured")

    saved_pin = doc.to_dict().get("login_pin")

    if payload.current_pin != saved_pin:
        raise HTTPException(status_code=401, detail="Current PIN is incorrect")

    # Validate new PIN
    if len(payload.new_pin) != 4 or not payload.new_pin.isdigit():
        raise HTTPException(status_code=400, detail="New PIN must be exactly 4 digits")

    if payload.current_pin == payload.new_pin:
        raise HTTPException(
            status_code=400, detail="New PIN must be different from current PIN"
        )

    # Update PIN in database
    db.collection("Login").document("pin").update({"login_pin": payload.new_pin})

    return {"success": True, "message": "PIN changed successfully"}
