from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    summary = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)  # Storing as JSON string or Text block
    education = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)      # Storing as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
