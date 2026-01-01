from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class CVResult(Base):
    __tablename__ = "cv_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    score = Column(Float)
