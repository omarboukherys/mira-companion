"""Long-term memory manager backed by Qdrant."""

import uuid

from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from mira.settings import settings

EMBEDDING_DIM = 384  # dimension of BAAI/bge-small-en-v1.5 vectors


class MemoryManager:
    """Stores and retrieves user facts as vectors in Qdrant."""

    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        self.embedder = TextEmbedding(model_name=settings.EMBEDDING_MODEL_NAME)
        self._ensure_collection()

    def _ensure_collection(self):
        """Create the collection on first run, skip if it already exists."""
        collections = [c.name for c in self.client.get_collections().collections]
        if settings.QDRANT_COLLECTION_NAME not in collections:
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM,
                    distance=Distance.COSINE,
                ),
            )

    def store_memory(self, text: str, user_id: str) -> None:
        """Embed a fact and store it in Qdrant, tagged with the user it belongs to."""
        vector = list(self.embedder.embed([text]))[0]

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload={"text": text, "user_id": user_id},
        )

        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=[point],
        )

    def retrieve_memories(self, query: str, user_id: str, top_k: int = 3) -> list[str]:
        """Find the facts most relevant to the query for this user."""
        query_vector = list(self.embedder.embed([query]))[0]

        results = self.client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_vector.tolist(),
            limit=top_k,
            query_filter={
                "must": [{"key": "user_id", "match": {"value": user_id}}]
            },
        )

        return [point.payload["text"] for point in results.points]


memory_manager = MemoryManager()