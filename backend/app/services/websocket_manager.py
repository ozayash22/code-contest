import asyncio
from collections import defaultdict
from typing import Dict, Set, Any

from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self._active: Dict[int, Set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, contest_id: int, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self._active[contest_id].add(websocket)

    def disconnect(self, contest_id: int, websocket: WebSocket):
        async def _remove():
            async with self._lock:
                conns = self._active.get(contest_id)
                if conns and websocket in conns:
                    conns.remove(websocket)
                    if not conns:
                        del self._active[contest_id]
        asyncio.create_task(_remove())

    async def broadcast(self, contest_id: int, message: Any):
        async with self._lock:
            conns = list(self._active.get(contest_id, ()))
        for ws in conns:
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(contest_id, ws)

manager = WebSocketManager()