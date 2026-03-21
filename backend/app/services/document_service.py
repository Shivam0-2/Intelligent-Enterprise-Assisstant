"""
DocumentService — handles PDF ingestion for both admin (policy) and employee (personal) flows.
Implementation will be added in the Document Processing step.
"""
from fastapi import UploadFile
from sqlalchemy.orm import Session


class DocumentService:

    @staticmethod
    async def process_policy_document(
        file: UploadFile, uploader: dict, db: Session
    ) -> dict:
        """
        Admin flow (persistent):
        1. Extract text from PDF
        2. Chunk text into segments
        3. Generate embeddings via EmbeddingService
        4. Store vectors in FAISS
        5. Save document record to SQLite
        """
        raise NotImplementedError("DocumentService.process_policy_document — coming in Document step")

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