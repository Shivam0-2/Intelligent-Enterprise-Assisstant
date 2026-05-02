"""
ChatService — orchestrates the RAG query pipeline.
"""

from app.services.embedding_service import EmbeddingService
from app.services.faiss_service import FaissService
from app.services.llm_service import LLMService
import numpy as np


class ChatService:

    @staticmethod
    def process_query(
        query: str,
        user: dict,
        top_k: int = 5,
        context: str = None
    ) -> dict:

        query_lower = query.lower().strip()

        # ---------------------------------
        # GREETINGS
        # ---------------------------------
        if query_lower in [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good evening",
            "good afternoon"
        ]:
            return {
                "query": query,
                "answer": "Hello! I'm your Enterprise Assistant. Ask me anything about company policies or documents."
            }

        # ---------------------------------
        # SMART PERSONAL DOC DETECTION
        # ---------------------------------
        personal_keywords = [
            "summarize",
            "summary",
            "this file",
            "uploaded file",
            "this pdf",
            "this report",
            "report",
            "keywords",
            "explain document",
            "what is this document"
        ]

        use_personal_doc = (
            context is not None
            and context.strip() != ""
            and any(k in query_lower for k in personal_keywords)
        )

        # =====================================================
        # PERSONAL DOCUMENT MODE (SMART)
        # =====================================================
        if use_personal_doc:

            prompt_context = context[:12000]

            answer = LLMService.generate_response(
                context=prompt_context,
                question=f"""
You are a document assistant.

Use ONLY the uploaded document context.

User Question:
{query}

Rules:
- Summarize clearly
- Use headings and bullet points
- Extract key insights
- If answer not available, say:
This information is not available in the uploaded file.
"""
            )

            return {
                "query": query,
                "answer": answer
            }

        # =====================================================
        # COMPANY DOCUMENT RAG MODE
        # =====================================================
        query_embedding = EmbeddingService.embed_chunks([query])[0]

        try:
            index = FaissService.load_index()

        except FileNotFoundError:
            return {
                "query": query,
                "answer": "No company documents have been uploaded yet."
            }

        # ---------------------------------
        # SEARCH
        # ---------------------------------
        retrieved_chunks = FaissService.search(
            index,
            query_embedding,
            top_k=top_k
        )

        if not retrieved_chunks:
            return {
                "query": query,
                "answer": "No relevant information found in company documents."
            }

        # ---------------------------------
        # RERANKING
        # ---------------------------------
        chunk_embeddings = EmbeddingService.embed_chunks(retrieved_chunks)

        def cosine_sim(a, b):
            return np.dot(a, b) / (
                np.linalg.norm(a) * np.linalg.norm(b)
            )

        scored = []

        for chunk, emb in zip(retrieved_chunks, chunk_embeddings):
            score = cosine_sim(query_embedding, emb)
            scored.append((score, chunk))

        scored.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        best_chunks = [chunk for _, chunk in scored[:3]]

        final_context = "\n\n".join(best_chunks)

        # ---------------------------------
        # FINAL LLM ANSWER (IMPROVED PROMPT)
        # ---------------------------------
        answer = LLMService.generate_response(
            context=final_context,
            question=f"""
You are an enterprise assistant.

Use ONLY the company document context.

User Question:
{query}

Rules:
- Answer professionally
- Use concise bullet points where useful
- Do NOT make up information
- If answer is not available, say:
This information is not available in company documents.
"""
        )

        return {
            "query": query,
            "answer": answer
        }