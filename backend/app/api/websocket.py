from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_manager import manager
from app.services.leaderboard_service import get_leaderboard

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/leaderboard/{contest_id}")
async def leaderboard_socket(
    websocket: WebSocket,
    contest_id: int
):
    await manager.connect(contest_id, websocket)

    try:
        data = get_leaderboard(contest_id)

        await websocket.send_json(data)

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(contest_id, websocket)