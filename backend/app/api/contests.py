from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.contest import Contest
from app.schemas.contest import ContestCreateSchema, ContestResponseSchema
from app.api.deps import admin_required

router = APIRouter(prefix="/api/contests", tags=["Contests"])


@router.post("/", response_model=ContestResponseSchema)
def create_contest(
    data: ContestCreateSchema,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    contest = Contest(
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    db.add(contest)
    db.commit()
    db.refresh(contest)
    return {
        "id": contest.id,
        "title": contest.title,
        "description": contest.description,
        "start_time": contest.start_time,
        "end_time": contest.end_time,
        "status": contest.status,
    }


@router.get("/", response_model=list[ContestResponseSchema])
def get_all_contests(db: Session = Depends(get_db)):
    contests = db.query(Contest).all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "start_time": c.start_time,
            "end_time": c.end_time,
            "status": c.status,
        }
        for c in contests
    ]


@router.get("/live", response_model=list[ContestResponseSchema])
def live_contests(db: Session = Depends(get_db)):
    contests = db.query(Contest).all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "start_time": c.start_time,
            "end_time": c.end_time,
            "status": c.status,
        }
        for c in contests if c.status == "LIVE"
    ]
