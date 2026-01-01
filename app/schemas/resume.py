from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class RankRequest(BaseModel):
    jd: str

class ResumeMatch(BaseModel):
    score: float
    metadata: Dict[str, Any]

class RankResponse(BaseModel):
    results: List[ResumeMatch]


class ResumeUploadResponse(BaseModel):
    status: str
    filename: str

class BatchUploadResponse(BaseModel):
    results: List[ResumeUploadResponse]

class Resume(BaseModel):
    id: int
    filename: str
    summary: str | None = None
    experience: str | None = None
    education: str | None = None
    skills: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
