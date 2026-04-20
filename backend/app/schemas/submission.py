from pydantic import BaseModel

class SubmissionCreateSchema(BaseModel):
    problem_id: int
    language: str
    code: str


class SubmissionResponseSchema(BaseModel):
    id: int
    user_id: int
    problem_id: int
    language: str
    status: str
    runtime: float

    passed_count: int = 0
    failed_count: int = 0
    total_tests: int = 0

    class Config:
        from_attributes = True