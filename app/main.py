from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import CVResult, Base
from app.service import extract_text, score_cv

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/rank")
async def rank_cvs(jd: str, files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    results = []

    for f in files:
        text = extract_text(f.file)
        score = score_cv(jd, text)

        record = CVResult(
            filename=f.filename,
            score=score
        )
        db.add(record)
        db.commit()

        results.append({
            "filename": f.filename,
            "score": round(score, 2)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {"ranking": results}


@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    return db.query(CVResult).order_by(CVResult.score.desc()).all()
