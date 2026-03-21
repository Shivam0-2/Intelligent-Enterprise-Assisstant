"""
ChatService — orchestrates the RAG query pipeline.
Implementation will be added in the RAG step.
"""


class ChatService:

    @staticmethod
    def process_query(query: str, user: dict) -> str:
        """
        1. Embed the query via EmbeddingService
        2. Search FAISS for top-k relevant chunks
        3. Build a prompt with context + query
        4. Call LLMService to generate a response
        5. Return the answer string
        """
        raise NotImplementedError("ChatService.process_query — coming in RAG step")