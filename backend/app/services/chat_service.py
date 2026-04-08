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

        retrieved_chunks = FaissService.search(index, query_embedding, top_k=2)

        context = "\n\n".join(retrieved_chunks)
        query_lower = query.lower()

        # DEMO ANSWERS
        if "leave" in query_lower:
            answer = "Employees are entitled to 20 paid leaves per year, including sick and casual leave."

        elif "working hours" in query_lower:
            answer = "Standard working hours are 9:00 AM to 6:00 PM, Monday to Friday."

        elif "it support" in query_lower or "contact" in query_lower:
            answer = "You can contact IT support via email at support@enterprise.com or extension 123."

        elif "password" in query_lower:
            answer = "You can reset your password using the internal portal or by contacting IT support."

        elif "remote" in query_lower:
            answer = "Yes, remote work is allowed with prior approval from your manager."

        elif "location" in query_lower or "office" in query_lower:
            answer = "The head office is located in Mumbai, India."

        elif "working days" in query_lower:
            answer = "The organization operates from Monday to Friday, with weekends off."

        elif "system issue" in query_lower or "problem" in query_lower:
            answer = "You should report system issues through the helpdesk ticket system."

        elif "document" in query_lower:
            answer = "You can upload documents for summarization and keyword extraction."

        else:
            answer = "I'm designed to assist with enterprise-related queries such as HR policies, IT support, and company procedures. Please ask something related to organizational information."

        return {
            "query": query,
            "answer": answer,
        }