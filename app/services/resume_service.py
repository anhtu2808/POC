from typing import List, Dict, Any
from app.services.embedding import embed_text
from app.db.vector import qdrant
from app.core.config import settings
import uuid
import pdfplumber
from sqlalchemy.orm import Session
from app.models.resume import Resume
import json
from app.services.llm_service import llm_service

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        return "".join(p.extract_text() or "" for p in pdf.pages)





def save_resume(db: Session, resume_text: str, metadata: dict):
    # 1. Parse Resume with LLM
    print("Parsing resume with LLM...")
    try:
        parsed_data = llm_service.extract_resume_data(resume_text)
        print("Parsing complete.")
    except Exception as e:
        print(f"LLM Parsing failed: {e}")
        parsed_data = {}

    # 2. Save to Vector DB
    vector = embed_text(resume_text)
    qdrant.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=[
            {
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": metadata
            }
        ]
    )

    # 3. Save to Reference DB (Postgres)
    db_resume = Resume(
        filename=metadata.get("filename"),
        content=resume_text,
        summary=parsed_data.get("summary"),
        experience=json.dumps(parsed_data.get("experience", [])),
        education=json.dumps(parsed_data.get("education", [])),
        skills=json.dumps(parsed_data.get("skills", []))
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_all_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resume).offset(skip).limit(limit).all()

def search_best_resumes(jd_text: str, limit=10) -> List[Dict[str, Any]]:
    jd_vector = embed_text(jd_text)

    results = qdrant.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=jd_vector,
        limit=limit
    ).points

    return [
        {
            "score": round(r.score * 100, 2),
            "metadata": r.payload
        }
        for r in results
    ]
