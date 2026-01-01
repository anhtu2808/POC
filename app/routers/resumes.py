from fastapi import APIRouter, UploadFile, File, Depends
from app.services.resume_service import save_resume, search_best_resumes, extract_text, get_all_resumes
from typing import List
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.resume import RankRequest, RankResponse, ResumeUploadResponse, BatchUploadResponse, Resume

router = APIRouter()

@router.post("/upload", response_model=BatchUploadResponse)
async def upload_resumes(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    uploaded_files = []
    for file in files:
        text = extract_text(file.file)
        save_resume(db, text, {"filename": file.filename})
        uploaded_files.append({"status": "ok", "filename": file.filename})
    
    return {"results": uploaded_files}

@router.get("/", response_model=List[Resume])
def list_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_resumes(db, skip=skip, limit=limit)

@router.post("/rank", response_model=RankResponse)
def rank_resumes(req: RankRequest):
    results = search_best_resumes(req.jd)
    return {
        "results": results
    }
