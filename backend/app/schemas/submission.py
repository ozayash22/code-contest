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

    class Config:
        from_attributes = True