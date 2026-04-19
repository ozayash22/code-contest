from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(Integer, ForeignKey("contests.id"), nullable=False)

    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)

    difficulty = Column(String(20), default="Easy")

    statement = Column(Text, nullable=False)
    constraints = Column(Text)
    input_format = Column(Text)
    output_format = Column(Text)

    time_limit = Column(Integer, default=1)   # seconds
    memory_limit = Column(Integer, default=256) # MB