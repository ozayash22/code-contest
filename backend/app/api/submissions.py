from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user

from app.models.problem import Problem
from app.models.submission import Submission

from app.schemas.submission import (
    SubmissionCreateSchema,
    SubmissionResponseSchema
)

from app.services.judge_service import judge_submission
from app.services.leaderboard_service import update_leaderboard
from app.services.websocket_manager import manager
from app.services.leaderboard_service import get_leaderboard
import asyncio

router = APIRouter(
    prefix="/api/submissions",
    tags=["Submissions"]
)


@router.post("/",
response_model=SubmissionResponseSchema)
def submit_code(
    data: SubmissionCreateSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    problem = db.query(Problem).filter(
        Problem.id == data.problem_id
    ).first()

    if not problem:
        raise HTTPException(404, "Problem not found")

    submission = Submission(
        user_id=int(user["sub"]),
        problem_id=data.problem_id,
        language=data.language,
        code=data.code,
        status="PENDING"
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    result = judge_submission(
        data.problem_id,
        data.language,
        data.code,
        db,
        stop_on_first_failure=False
    )

    submission.status = result.get("status", "ERROR")
    submission.runtime = result.get("runtime", 0)

    db.commit()
    db.refresh(submission)

    if submission.status == "ACCEPTED":
        update_leaderboard(
            contest_id=problem.contest_id,
            user_id=submission.user_id,
            problem_id=problem.id,
            runtime=submission.runtime
        )
        leaderboard = get_leaderboard(problem.contest_id)

        asyncio.create_task(
            manager.broadcast(
                problem.contest_id,
                leaderboard
            )
        )

    return {
        "id": submission.id,
        "user_id": submission.user_id,
        "problem_id": submission.problem_id,
        "language": submission.language,
        "status": submission.status,
        "runtime": submission.runtime,
        "passed_count": result.get("passed_count", 0),
        "failed_count": result.get("failed_count", 0),
        "total_tests": result.get("total", 0)
    }


@router.get("/my")
def my_submissions(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Submission).filter(
        Submission.user_id == int(user["sub"])
    ).all()