import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
from app.embedding import embed_text
from app.vector_db import qdrant, COLLECTION_NAME
import uuid

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for p in pdf.pages:
            text += p.extract_text() or ""
    return text

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def score_cv(jd, cv_text):
    jd_vec = model.encode(jd)
    cv_vec = model.encode(cv_text)
    return float(cosine_sim(jd_vec, cv_vec) * 100)


def save_cv_vector(cv_text: str, metadata: dict):
    vector = embed_text(cv_text)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": metadata
            }
        ]
    )

def search_best_cvs(jd_text: str, limit=10):
    jd_vector = embed_text(jd_text)

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
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

