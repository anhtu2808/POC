from qdrant_client import QdrantClient
from app.core.config import settings

qdrant = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT
)

def init_collection():
    collections = qdrant.get_collections().collections
    if settings.QDRANT_COLLECTION not in [c.name for c in collections]:
        qdrant.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config={
                "size": settings.VECTOR_SIZE,
                "distance": "Cosine"
            }
        )
