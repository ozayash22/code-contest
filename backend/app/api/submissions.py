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
        data.code,
        data.language,
        data.problem_id,
        db
    )

    submission.status = result["status"]
    submission.runtime = result["runtime"]

    db.commit()
    db.refresh(submission)

    return submission


@router.get("/my")
def my_submissions(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Submission).filter(
        Submission.user_id == int(user["sub"])
    ).all()