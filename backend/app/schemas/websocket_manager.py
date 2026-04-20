from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.rooms = {}

    async def connect(self, contest_id: int, websocket: WebSocket):
        await websocket.accept()

        if contest_id not in self.rooms:
            self.rooms[contest_id] = []

        self.rooms[contest_id].append(websocket)

    def disconnect(self, contest_id: int, websocket: WebSocket):
        if contest_id in self.rooms:
            self.rooms[contest_id].remove(websocket)

    async def broadcast(self, contest_id: int, data):
        if contest_id in self.rooms:
            dead = []

            for ws in self.rooms[contest_id]:
                try:
                    await ws.send_json(data)
                except:
                    dead.append(ws)

            for ws in dead:
                self.rooms[contest_id].remove(ws)


manager = ConnectionManager()