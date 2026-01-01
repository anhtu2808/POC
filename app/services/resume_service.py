from typing import List, Dict, Any
from app.services.embedding import embed_text
from app.db.vector import qdrant
from app.core.config import settings
import uuid
import pdfplumber

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        return "".join(p.extract_text() or "" for p in pdf.pages)

def save_resume_vector(resume_text: str, metadata: dict):
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
