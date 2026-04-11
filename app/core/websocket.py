# app/core/websocket.py

from fastapi import WebSocket
from typing import Dict, List
from app.utils.logger import logger


class ConnectionManager:
    """
    Centralized WebSocket connection manager.

    Responsibilities:
    - Track active WebSocket connections
    - Send messages to specific users
    - Broadcast messages by user type
    - Clean up disconnected sockets

    This manager DOES NOT:
    - Manually close sockets
    - Handle business logic
    - Persist anything
    """

    def __init__(self) -> None:
        # Structure:
        # {
        #   "workers": {
        #       "worker_id": [WebSocket, WebSocket]
        #   },
        #   "companies": {
        #       "company_id": [WebSocket]
        #   }
        # }
        self.active_connections: Dict[str, Dict[str, List[WebSocket]]] = {
            "workers": {},
            "companies": {},
        }

    # --------------------------------------------------
    # CONNECT
    # --------------------------------------------------
    async def connect(
        self,
        user_type: str,
        user_id: str,
        websocket: WebSocket,
    ) -> None:
        """
        Accept and register a new WebSocket connection.
        """
        await websocket.accept()

        self.active_connections.setdefault(user_type, {})
        self.active_connections[user_type].setdefault(user_id, [])

        self.active_connections[user_type][user_id].append(websocket)

        logger.info(f"{user_type} {user_id} connected.")

    # --------------------------------------------------
    # DISCONNECT
    # --------------------------------------------------
    async def disconnect(
        self,
        user_type: str,
        user_id: str,
        websocket: WebSocket,
    ) -> None:
        """
        Remove a WebSocket connection from active tracking.
        Does NOT call websocket.close().
        """
        try:
            connections = self.active_connections.get(user_type, {}).get(user_id)

            if not connections:
                return

            if websocket in connections:
                connections.remove(websocket)

            # Cleanup empty user bucket
            if not connections:
                self.active_connections[user_type].pop(user_id, None)

            logger.info(f"{user_type} {user_id} disconnected.")

        except Exception as e:
            logger.error(f"Disconnect cleanup error: {e}")

    # --------------------------------------------------
    # SEND TO SINGLE USER
    # --------------------------------------------------
    async def send_to_user(
        self,
        user_type: str,
        user_id: str,
        message: dict,
    ) -> None:
        """
        Send a JSON message to all active sockets of a user.
        Automatically removes broken sockets.
        """

        # logger.info(
        #     "WS CHECK → %s %s → connections=%s",
        #     user_type,
        #     user_id,
        #     len(connections) if connections else 0,
        # )
        connections = self.active_connections.get(user_type, {}).get(user_id)

        if not connections:
            logger.debug(f"{user_type} {user_id} not connected.")
            return

        dead_connections = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                dead_connections.append(websocket)

        # Cleanup dead sockets
        for ws in dead_connections:
            await self.disconnect(user_type, user_id, ws)

    # --------------------------------------------------
    # BROADCAST BY USER TYPE
    # --------------------------------------------------
    async def broadcast(
        self,
        user_type: str,
        message: dict,
    ) -> None:
        """
        Broadcast a message to all users under a user type.
        """
        user_ids = list(self.active_connections.get(user_type, {}).keys())

        for user_id in user_ids:
            await self.send_to_user(user_type, user_id, message)


# Singleton instance
manager = ConnectionManager()
