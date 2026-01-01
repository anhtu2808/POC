from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class ResumeResult(Base):
    __tablename__ = "resume_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    score = Column(Float)
