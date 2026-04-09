import asyncio
from typing import Any

from firebase_admin import exceptions as firebase_exceptions
from firebase_admin import messaging


from app.core.firebase_auth import initialize_firebase
from app.utils.logger import logger


def _stringify_payload(data: dict[str, Any]) -> dict[str, str]:
    return {
        str(key): "" if value is None else str(value) for key, value in data.items()
    }


async def send_fcm_notification(
    token: str,
    data: dict[str, Any],
    title: str = "New Job Available",
    body: str = "",
) -> None:
    """
    Send FCM push notification with both notification + data payload.
    """
    if not token:
        logger.warning("Skipping FCM send: empty token")
        return

    payload = _stringify_payload(data)
    resolved_body = body or f"Wage: {payload.get('wage', '')} | {payload.get('work_address', '')}"
    notification = messaging.Notification(title=title, body=resolved_body)

    message = messaging.Message(
        token=token,
        notification=notification,
        data=payload,
    )

    try:
        initialize_firebase()
        response = await asyncio.to_thread(messaging.send, message)
        logger.info("FCM notification sent successfully: %s", response)
    except messaging.UnregisteredError:
        logger.warning("FCM token is invalid/unregistered. token=%s", token)
    except firebase_exceptions.InvalidArgumentError:
        logger.warning(
            "FCM request rejected due to invalid token/payload. token=%s", token
        )
    except firebase_exceptions.FirebaseError as exc:
        logger.error("FCM send failed for token=%s: %s", token, exc)
    except Exception:
        logger.exception("Unexpected error while sending FCM notification")
