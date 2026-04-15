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
        try:
            contents = await file.read()

            extracted_pages = []
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_pages.append(text)

            # --- FULL TEXT ---
            full_text = "\n".join(extracted_pages)

            # --- CLEAN TEXT ---
            full_text = full_text.replace("\n\n", "\n")
            full_text = full_text.replace("\t", " ")

            # --- PARAGRAPH-BASED CHUNKING ---
            def chunk_text(text: str, max_chars: int = 800):
                paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

                chunks = []
                current_chunk = ""

                for para in paragraphs:
                    if len(current_chunk) + len(para) <= max_chars:
                        current_chunk += " " + para
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = para

                if current_chunk:
                    chunks.append(current_chunk.strip())

                return chunks

            chunks = chunk_text(full_text)

            # --- VALIDATION ---
            if not chunks:
                raise ValueError("No text chunks found. PDF may be empty.")

            # --- EMBEDDINGS ---
            embeddings = await asyncio.to_thread(
                EmbeddingService.embed_chunks, chunks
            )

            # --- FAISS ---
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
                detail=f"Failed to process PDF: {str(e)}"
            )

    @staticmethod
    async def process_personal_document(file: UploadFile) -> dict:
        raise NotImplementedError("Coming next")