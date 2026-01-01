from fastapi import FastAPI
from app.routers import resumes
from app.core.config import settings
from app.db.vector import init_collection

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
def startup_event():
    init_collection()

app.include_router(resumes.router, prefix=f"{settings.API_V1_STR}/resumes", tags=["resumes"])