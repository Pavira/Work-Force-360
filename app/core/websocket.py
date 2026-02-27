# app/core/websocket.py  # Identifies this file's module path.

from fastapi import (
    WebSocket,
    WebSocketDisconnect,
)  # Imports FastAPI WebSocket classes for connection handling.
from typing import Dict, List  # Imports typing helpers used for nested connection maps.
import asyncio  # Imports asyncio utilities for background heartbeat tasks.
from utils.logger import logger  # Imports shared application logger for observability.


class ConnectionManager:  # Defines a manager responsible for tracking and messaging socket clients.
    def __init__(self):  # Initializes in-memory state for active websocket connections.
        self.active_connections: Dict[str, Dict[str, List[WebSocket]]] = (
            {  # Maps user type -> user id -> list of websocket sessions.
                "workers": {},  # Stores worker user socket lists keyed by worker id.
                "companies": {},  # Stores company user socket lists keyed by company id.
            }
        )  # Ends active connection map initialization.
        self.heartbeat_interval = (
            30  # seconds  # Sets heartbeat frequency to keep connections alive.
        )

    # -------------------------
    # CONNECT
    # -------------------------
    async def connect(
        self, user_type: str, user_id: str, websocket: WebSocket
    ):  # Accepts and registers a new websocket for a user.
        await websocket.accept()  # Performs the websocket handshake acceptance.

        if (
            user_id not in self.active_connections[user_type]
        ):  # Creates a user bucket if this is their first active socket.
            self.active_connections[user_type][
                user_id
            ] = []  # Initializes empty socket list for this user id.

        self.active_connections[user_type][user_id].append(
            websocket
        )  # Appends the current socket to this user's active sessions.

        logger.info(
            f"{user_type} {user_id} connected."
        )  # Logs successful connection registration.

        asyncio.create_task(
            self._heartbeat(websocket, user_type, user_id)
        )  # Starts background heartbeat for this socket.

    # -------------------------  # Section divider for disconnect logic.
    # DISCONNECT  # Labels the disconnect method section.
    # -------------------------  # Section divider end.
    async def disconnect(
        self, user_type: str, user_id: str, websocket: WebSocket
    ):  # Removes and closes a websocket connection safely.
        try:  # Protects disconnect flow from unexpected runtime errors.
            connections = self.active_connections[user_type].get(
                user_id
            )  # Fetches current socket list for the given user.

            if (
                connections and websocket in connections
            ):  # Ensures the target socket exists before removing it.
                connections.remove(
                    websocket
                )  # Removes this socket from the user's active list.

                if (
                    not connections
                ):  # Checks whether user has no remaining active sockets.
                    self.active_connections[user_type].pop(
                        user_id
                    )  # Cleans up empty user key to keep state compact.

            await websocket.close()  # Attempts to close the websocket gracefully.

            logger.info(
                f"{user_type} {user_id} disconnected safely."
            )  # Logs successful disconnect completion.

        except (
            Exception
        ) as e:  # Captures any failure that occurs during disconnect steps.
            logger.error(
                f"Error during disconnect: {e}"
            )  # Logs disconnect failure details for debugging.

    # -------------------------
    # SEND TO ONE USER
    # -------------------------
    async def send_to_user(
        self, user_type: str, user_id: str, message: dict
    ):  # Sends one JSON message to all sockets of a specific user.
        connections = self.active_connections[user_type].get(
            user_id
        )  # Looks up all active sockets for the target user.

        if (
            not connections
        ):  # Exits early when user has no active websocket connections.
            logger.warning(
                f"{user_type} {user_id} not connected."
            )  # Records that delivery could not proceed due to no connection.
            return  # Stops execution because there are no sockets to send to.

        dead_connections = []  # Collects sockets that fail send attempts for cleanup.

        for (
            websocket
        ) in connections:  # Iterates through each active socket for this user.
            try:  # Wraps each send attempt to isolate socket-level failures.
                await websocket.send_json(
                    message
                )  # Sends the JSON payload over the websocket.
            except Exception as e:  # Handles send failure for this specific socket.
                logger.error(f"Send failed: {e}")  # Logs send exception details.
                dead_connections.append(
                    websocket
                )  # Marks this socket to be disconnected afterward.

        # Remove broken connections  # Explains cleanup of sockets that failed sending.
        for ws in dead_connections:  # Iterates over sockets identified as broken.
            await self.disconnect(
                user_type, user_id, ws
            )  # Disconnects each broken socket and updates manager state.

    # -------------------------
    # BROADCAST
    # -------------------------
    async def broadcast(
        self, user_type: str, message: dict
    ):  # Sends a message to every user id under one user type.
        for user_id in list(
            self.active_connections[user_type].keys()
        ):  # Iterates over a snapshot of user ids to avoid dict mutation issues.
            await self.send_to_user(
                user_type, user_id, message
            )  # Reuses per-user send logic for each user id.

    # -------------------------  # Section divider for heartbeat logic.
    # HEARTBEAT  # Labels keep-alive heartbeat background task.
    # -------------------------  # Section divider end.
    async def _heartbeat(
        self, websocket: WebSocket, user_type: str, user_id: str
    ):  # Periodically pings client to detect stale connections.
        try:  # Protects heartbeat loop so failures trigger cleanup.
            while True:  # Runs continuously for lifetime of this websocket.
                await asyncio.sleep(
                    self.heartbeat_interval
                )  # Waits configured interval between heartbeat pings.
                await websocket.send_json(
                    {"type": "PING"}
                )  # Sends ping message to keep connection active and verify liveness.
        except (
            Exception
        ):  # Handles any heartbeat loop failure, usually closed or broken socket.
            await self.disconnect(
                user_type, user_id, websocket
            )  # Performs disconnect cleanup when heartbeat fails.


manager = (
    ConnectionManager()
)  # Creates shared singleton manager instance for application use.
