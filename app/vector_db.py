from qdrant_client import QdrantClient
import os

# Nếu chạy local thì host là 'localhost', nếu sau này chạy docker thì dùng biến môi trường
qdrant_host = os.getenv("QDRANT_HOST", "localhost")

qdrant = QdrantClient(
    host=qdrant_host,
    port=6333
)

COLLECTION_NAME = "cv_embeddings"

def init_collection(vector_size: int):
    collections = qdrant.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={
                "size": vector_size,
                "distance": "Cosine"
            }
        )