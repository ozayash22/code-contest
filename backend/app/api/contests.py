from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.contest import Contest
from app.schemas.contest import ContestCreateSchema
from app.api.deps import admin_required

router = APIRouter(prefix="/api/contests", tags=["Contests"])


@router.post("/")
def create_contest(
    data: ContestCreateSchema,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    contest = Contest(
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time
    )

    db.add(contest)
    db.commit()
    db.refresh(contest)

    return contest


@router.get("/")
def get_all_contests(db: Session = Depends(get_db)):
    contests = db.query(Contest).all()

    now = datetime.utcnow()

    for contest in contests:
        if now < contest.start_time:
            contest.status = "UPCOMING"
        elif contest.start_time <= now <= contest.end_time:
            contest.status = "LIVE"
        else:
            contest.status = "COMPLETED"

    return contests


@router.get("/live")
def live_contests(db: Session = Depends(get_db)):
    now = datetime.utcnow()

    contests = db.query(Contest).filter(
        Contest.start_time <= now,
        Contest.end_time >= now
    ).all()

    return contests