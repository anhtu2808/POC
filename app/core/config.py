from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume Ranking API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://cvuser:cvpass@localhost:5432/cvdb"
    
    # QdrantVectorDB
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "resume_embeddings"
    VECTOR_SIZE: int = 384  # all-MiniLM-L6-v2 dimension

    # Local LLM
    MODEL_PATH: str = "llm/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
    MAX_TOKENS: int = 2048

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
