from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.schemas.test_case import (
    TestCaseCreateSchema,
    TestCaseResponseSchema
)
from app.api.deps import admin_required

router = APIRouter(
    prefix="/api/test-cases",
    tags=["Test Cases"]
)


@router.post("/",
response_model=TestCaseResponseSchema)
def create_test_case(
    data: TestCaseCreateSchema,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    problem = db.query(Problem).filter(
        Problem.id == data.problem_id
    ).first()

    if not problem:
        raise HTTPException(404, "Problem not found")

    test_case = TestCase(
        problem_id=data.problem_id,
        input_data=data.input_data,
        expected_output=data.expected_output,
        is_hidden=data.is_hidden
    )

    db.add(test_case)
    db.commit()
    db.refresh(test_case)

    return test_case


@router.get("/problem/{problem_id}",
response_model=list[TestCaseResponseSchema])
def get_visible_test_cases(
    problem_id: int,
    db: Session = Depends(get_db)
):
    return db.query(TestCase).filter(
        TestCase.problem_id == problem_id,
        TestCase.is_hidden == False
    ).all()