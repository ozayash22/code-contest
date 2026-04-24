from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from slugify import slugify
from app.core.database import get_db
from app.models.problem import Problem
from app.models.contest import Contest
from app.schemas.problem import (
    ProblemCreateSchema,
    ProblemResponseSchema
)
from app.api.deps import admin_required

router = APIRouter(prefix="/api/problems", tags=["Problems"])

@router.post("/", response_model=ProblemResponseSchema)
def create_problem(
    data: ProblemCreateSchema,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    contest = db.query(Contest).filter(
        Contest.id == data.contest_id
    ).first()

    if not contest:
        raise HTTPException(404, "Contest not found")

    slug = slugify(data.title)

    problem = Problem(
        contest_id=data.contest_id,
        title=data.title,
        slug=slug,
        difficulty=data.difficulty,
        statement=data.statement,
        constraints=data.constraints,
        input_format=data.input_format,
        output_format=data.output_format,
        time_limit=data.time_limit,
        memory_limit=data.memory_limit
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    return problem


@router.get("/contest/{contest_id}",
response_model=list[ProblemResponseSchema])
def get_contest_problems(
    contest_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Problem).filter(
        Problem.contest_id == contest_id
    ).all()

@router.get("/{problem_id}",
response_model=ProblemResponseSchema)
def get_problem(problem_id: int,
db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:
        raise HTTPException(404, "Problem not found")

    return problem