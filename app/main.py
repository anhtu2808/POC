from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.service import save_cv_vector, search_best_cvs
from app.vector_db import init_collection
import pdfplumber

app = FastAPI()

@app.on_event("startup")
def startup():
    init_collection(384)  # dimension of MiniLM

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        return "".join(p.extract_text() or "" for p in pdf.pages)

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    text = extract_text(file.file)
    save_cv_vector(text, {"filename": file.filename})
    return {"status": "ok"}

class RankRequest(BaseModel):
    jd: str

@app.post("/rank")
def rank_cvs(req: RankRequest):
    return {
        "results": search_best_cvs(req.jd)
    }