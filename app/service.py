import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer

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
