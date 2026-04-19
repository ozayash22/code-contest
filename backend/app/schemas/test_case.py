from pydantic import BaseModel

class TestCaseCreateSchema(BaseModel):
    problem_id: int
    input_data: str
    expected_output: str
    is_hidden: bool = True


class TestCaseResponseSchema(BaseModel):
    id: int
    problem_id: int
    input_data: str
    expected_output: str
    is_hidden: bool

    class Config:
        from_attributes = True