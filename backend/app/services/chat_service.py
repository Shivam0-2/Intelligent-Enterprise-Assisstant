"""
ChatService — orchestrates the RAG query pipeline.
"""
from app.services.embedding_service import EmbeddingService
from app.services.faiss_service import FaissService


class ChatService:

    @staticmethod
    def process_query(query: str, user: dict, top_k: int = 5) -> dict:
        """
        1. Embed the query
        2. Load FAISS index
        3. Search for top-k similar chunks
        4. Return retrieved chunks
        """
        query_embedding = EmbeddingService.embed_chunks([query])[0]

        try:
            index = FaissService.load_index()
        except FileNotFoundError:
            return {
                "query": query,
                "retrieved_chunks": [],
                "error": "No documents indexed yet. Please ask an admin to upload documents first.",
            }

        retrieved_chunks = FaissService.search(index, query_embedding, top_k=top_k)

        return {
            "query": query,
            "retrieved_chunks": retrieved_chunks,
            "total_retrieved": len(retrieved_chunks),
        }