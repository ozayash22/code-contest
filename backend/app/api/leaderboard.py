from fastapi import APIRouter
from app.services.leaderboard_service import get_leaderboard

router = APIRouter(
    prefix="/api/leaderboard",
    tags=["Leaderboard"]
)


@router.get("/{contest_id}")
def leaderboard(contest_id: int):
    return get_leaderboard(contest_id)