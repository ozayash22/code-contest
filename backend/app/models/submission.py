from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    problem_id = Column(Integer, nullable=False)

    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)

    status = Column(String(30), default="PENDING")

    runtime = Column(Float, default=0)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())