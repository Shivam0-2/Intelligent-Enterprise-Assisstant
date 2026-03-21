"""
DocumentService — handles PDF ingestion.
"""
import os
import pdfplumber
import io
import asyncio
from fastapi import UploadFile, HTTPException
from app.services.embedding_service import EmbeddingService
from app.services.faiss_service import FaissService
from app.config import get_settings

settings = get_settings()
INDEX_PATH = settings.faiss_index_path + "/index.faiss"


class DocumentService:

    @staticmethod
    async def process_policy_document(
        file: UploadFile, uploader: dict, db
    ) -> dict:
        """
        Reads the uploaded PDF and extracts raw text page by page.
        Returns the full text and a short preview.
        """
        try:
            contents = await file.read()

            extracted_pages = []
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_pages.append(text)

            full_text = "\n".join(extracted_pages)

            # --- Chunking ---
            chunk_size = 500
            overlap = 100

            if overlap >= chunk_size:
                raise ValueError(f"overlap ({overlap}) must be less than chunk_size ({chunk_size})")

            chunks = []
            start = 0
            while start < len(full_text):
                end = start + chunk_size
                chunks.append(full_text[start:end])
                start += chunk_size - overlap

            # --- Embeddings ---
            if not chunks:
                raise ValueError("No text chunks found. The PDF may be empty or unreadable.")

            embeddings = await asyncio.to_thread(EmbeddingService.embed_chunks, chunks)

            # --- FAISS: load existing index or create new one ---
            dim = len(embeddings[0])
            if os.path.exists(INDEX_PATH):
                index = FaissService.load_index()
            else:
                index = FaissService.create_index(dim)

            result = FaissService.add_embeddings(index, embeddings, chunks)
            FaissService.save_index(index)

            return {
                "filename": file.filename,
                "total_pages": len(extracted_pages),
                "total_chunks": len(chunks),
                "embedding_dim": dim,
                "total_vectors_in_index": result["total_vectors"],
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract text from PDF: {str(e)}"
            )

    @staticmethod
    async def process_personal_document(file: UploadFile) -> dict:
        """
        Employee flow (temporary / not stored):
        1. Extract text from PDF
        2. Send text to LLMService for summarization
        3. Send text to LLMService for keyword extraction
        4. Return results — no DB writes
        """
        raise NotImplementedError("DocumentService.process_personal_document — coming in Document step")