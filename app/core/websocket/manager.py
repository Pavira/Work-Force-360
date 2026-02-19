class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, worker_id, websocket):
        await websocket.accept()
        self.active_connections[worker_id] = websocket

    async def send_job(self, worker_id, data):
        ws = self.active_connections.get(worker_id)
        if ws:
            await ws.send_json(data)

    def disconnect(self, worker_id):
        self.active_connections.pop(worker_id, None)
