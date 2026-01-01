from fastapi import APIRouter, UploadFile, File
from app.services.resume_service import save_resume_vector, search_best_resumes, extract_text
from app.schemas.resume import RankRequest, RankResponse, ResumeUploadResponse

router = APIRouter()

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text(file.file)
    save_resume_vector(text, {"filename": file.filename})
    return {"status": "ok"}

@router.post("/rank", response_model=RankResponse)
def rank_resumes(req: RankRequest):
    results = search_best_resumes(req.jd)
    return {
        "results": results
    }
