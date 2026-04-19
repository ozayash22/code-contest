from pydantic import BaseModel
from datetime import datetime

class ContestCreateSchema(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class ContestResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        from_attributes = True