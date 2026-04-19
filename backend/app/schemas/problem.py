from pydantic import BaseModel

class ProblemCreateSchema(BaseModel):
    contest_id: int
    title: str
    difficulty: str
    statement: str
    constraints: str
    input_format: str
    output_format: str
    time_limit: int
    memory_limit: int


class ProblemResponseSchema(BaseModel):
    id: int
    contest_id: int
    title: str
    slug: str
    difficulty: str
    statement: str
    constraints: str
    input_format: str
    output_format: str
    time_limit: int
    memory_limit: int

    class Config:
        from_attributes = True