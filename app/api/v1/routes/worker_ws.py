from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.concurrency import run_in_threadpool
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from uuid import UUID
from app.utils.logger import logger

from app.db.session import get_db
from app.core.websocket import manager
from app.models.job_model import JobPostingModel
from app.models.worker_models import WorkerRegistrationModel

router = APIRouter()


# -----------------------------
# DB HELPERS (SYNC)
# -----------------------------
def set_worker_online(db: Session, worker_id: UUID):
    logger.debug("set_worker_online called for worker_id=%s", worker_id)
    try:
        worker = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.id == worker_id)
            .first()
        )

        if worker:
            worker.is_online = True
            worker.is_available = True
            db.commit()
            logger.info("Worker %s marked online and available", worker_id)
        else:
            logger.warning("Worker %s not found while setting online", worker_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("DB error while setting worker %s online", worker_id)
        raise


def set_worker_offline(db: Session, worker_id: UUID):
    logger.debug("set_worker_offline called for worker_id=%s", worker_id)
    try:
        worker = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.id == worker_id)
            .first()
        )

        if worker:
            worker.is_online = False
            worker.is_available = False
            db.commit()
            logger.info("Worker %s marked offline and unavailable", worker_id)
        else:
            logger.warning("Worker %s not found while setting offline", worker_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("DB error while setting worker %s offline", worker_id)
        raise


def update_worker_location(db: Session, worker_id: UUID, lat: float, lng: float):
    logger.debug(
        "update_worker_location called for worker_id=%s lat=%s lng=%s",
        worker_id,
        lat,
        lng,
    )
    try:
        worker = (
            db.query(WorkerRegistrationModel)
            .filter(WorkerRegistrationModel.id == worker_id)
            .first()
        )

        if worker:
            point = from_shape(Point(lng, lat), srid=4326)
            worker.location = point
            db.commit()
            logger.info("Worker %s location updated - location - %s", worker_id, point)
        else:
            logger.warning("Worker %s not found while updating location", worker_id)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("DB error while updating location for worker %s", worker_id)
        raise


# -----------------------------
# WEBSOCKET ENDPOINT
# -----------------------------
@router.websocket("/{worker_id}")
async def worker_websocket(
    websocket: WebSocket,
    worker_id: UUID,
    db: Session = Depends(get_db),
):
    logger.info("Worker websocket connect requested for worker_id=%s", worker_id)
    await manager.connect("workers", worker_id, websocket)
    await websocket.send_json({"type": "CONNECTED", "worker_id": str(worker_id)})
    logger.info("Worker websocket connected for worker_id=%s", worker_id)

    # Mark worker online
    await run_in_threadpool(set_worker_online, db, worker_id)
    logger.debug("Initial online status update done for worker_id=%s", worker_id)

    try:
        while True:
            data = await websocket.receive_json()
            logger.debug("Worker %s websocket payload received: %s", worker_id, data)

            message_type = data.get("type")
            logger.debug("Worker %s message_type=%s", worker_id, message_type)

            # -------------------------
            # LOCATION UPDATE
            # -------------------------
            if message_type == "LOCATION_UPDATE":
                lat = data.get("lat")
                lng = data.get("lng")

                if lat is None or lng is None:
                    logger.warning(
                        "Worker %s LOCATION_UPDATE missing lat/lng payload=%s",
                        worker_id,
                        data,
                    )
                    continue

                await run_in_threadpool(
                    update_worker_location,
                    db,
                    worker_id,
                    lat,
                    lng,
                )
                logger.debug("Worker %s LOCATION_UPDATE processed", worker_id)

            # -------------------------
            # SET AVAILABLE
            # -------------------------
            elif message_type == "SET_AVAILABLE":
                await run_in_threadpool(set_worker_online, db, worker_id)
                logger.debug("Worker %s SET_AVAILABLE processed", worker_id)

            # -------------------------
            # SET UNAVAILABLE
            # -------------------------
            elif message_type == "SET_UNAVAILABLE":
                await run_in_threadpool(set_worker_offline, db, worker_id)
                logger.debug("Worker %s SET_UNAVAILABLE processed", worker_id)

            # -------------------------
            # GO OFFLINE
            # -------------------------
            elif message_type == "GO_OFFLINE":
                logger.info("Worker %s requested offline", worker_id)

                # mark offline in DB
                await run_in_threadpool(set_worker_offline, db, worker_id)

                await websocket.close()
                break

            # -------------------------
            # HEARTBEAT RESPONSE
            # -------------------------
            # elif message_type == "PONG":
            #     logger.debug("Worker %s heartbeat PONG received", worker_id)

            else:
                logger.warning(
                    "Unknown message type from worker %s: %s payload=%s",
                    worker_id,
                    message_type,
                    data,
                )

    except WebSocketDisconnect:
        logger.info("Worker websocket disconnected for worker_id=%s", worker_id)

    except Exception as e:
        logger.exception("Worker websocket error for worker_id=%s: %s", worker_id, e)

    finally:
        logger.debug("Worker websocket cleanup started for worker_id=%s", worker_id)
        await manager.disconnect("workers", worker_id, websocket)
        await run_in_threadpool(set_worker_offline, db, worker_id)
        logger.info("Worker websocket cleanup completed for worker_id=%s", worker_id)
