from pydantic import BaseModel
from typing import List, Dict, Any

class RankRequest(BaseModel):
    jd: str

class ResumeMatch(BaseModel):
    score: float
    metadata: Dict[str, Any]

class RankResponse(BaseModel):
    results: List[ResumeMatch]

class ResumeUploadResponse(BaseModel):
    status: str
