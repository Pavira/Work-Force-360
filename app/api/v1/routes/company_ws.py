from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool
from uuid import UUID


from app.db.session import get_db
from app.core.websocket import manager
from app.models.company_models import CompanyModel
from app.utils.logger import logger

router = APIRouter()


# -----------------------------
# WEBSOCKET ENDPOINT
# -----------------------------
@router.websocket("/{company_id}")
async def company_websocket(
    websocket: WebSocket,
    company_id: UUID,
    db: Session = Depends(get_db),
):
    logger.info("Company websocket connect requested for company_id=%s", company_id)
    await manager.connect("companies", str(company_id), websocket)
    logger.info("Company websocket connected for company_id=%s", company_id)

    try:
        while True:
            data = await websocket.receive_json()
            logger.debug("Company %s websocket payload received: %s", company_id, data)

            message_type = data.get("type")
            logger.debug("Company %s message_type=%s", company_id, message_type)

            # -------------------------
            # HEARTBEAT RESPONSE
            # -------------------------
            if message_type == "PONG":
                logger.debug("Company %s heartbeat PONG received", company_id)

            # -------------------------
            # OPTIONAL: CANCEL JOB
            # -------------------------
            elif message_type == "CANCEL_JOB":
                job_id = data.get("job_id")
                logger.info(
                    "Company %s requested CANCEL_JOB job_id=%s", company_id, job_id
                )
                # future logic

            else:
                logger.warning(
                    "Unknown message type from company %s: %s payload=%s",
                    company_id,
                    message_type,
                    data,
                )

    except WebSocketDisconnect:
        logger.info("Company websocket disconnected for company_id=%s", company_id)

    except Exception as e:
        logger.exception("Company websocket error for company_id=%s: %s", company_id, e)

    finally:
        logger.debug("Company websocket cleanup started for company_id=%s", company_id)
        await manager.disconnect("companies", str(company_id), websocket)
        logger.info("Company websocket cleanup completed for company_id=%s", company_id)
