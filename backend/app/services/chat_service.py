"""
ChatService — orchestrates the RAG query pipeline.
"""
from app.services.embedding_service import EmbeddingService
from app.services.faiss_service import FaissService
from app.services.llm_service import LLMService


class ChatService:

    @staticmethod
    def process_query(query: str, user: dict, top_k: int = 3) -> dict:
        query_embedding = EmbeddingService.embed_chunks([query])[0]

        try:
            index = FaissService.load_index()
        except FileNotFoundError:
            return {
                "query": query,
                "answer": "No documents indexed yet. Please ask an admin to upload documents first.",
            }

        retrieved_chunks = FaissService.search(index, query_embedding, top_k=5)

        context = "\n\n".join(retrieved_chunks)
        query_lower = query.lower()

        answer = LLMService.generate_response(context=context, question=query)
        return {
            "query": query,
            "answer": answer,
        }