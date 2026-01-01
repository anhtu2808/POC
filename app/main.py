from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import resumes
from app.core.config import settings
from app.db.vector import init_collection
from app.db.database import engine, Base
from app.models import resume  # noqa: F401

app = FastAPI(title=settings.PROJECT_NAME)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.on_event("startup")
def startup_event():
    Base.metadata.drop_all(bind=engine) # POC: Drop all to apply schema changes
    Base.metadata.create_all(bind=engine)
    init_collection()

app.include_router(resumes.router, prefix=f"{settings.API_V1_STR}/resumes", tags=["resumes"])