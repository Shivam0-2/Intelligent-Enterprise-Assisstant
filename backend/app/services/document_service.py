"""
DocumentService — handles PDF ingestion.
Step 1: Extract raw text only.
"""
import pdfplumber
import io
from fastapi import UploadFile, HTTPException


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
                    text = page.extract_text() or ""
                    if text:
                        extracted_pages.append(text)

            full_text = "\n".join(extracted_pages)

            return {
                "filename": file.filename,
                "total_pages": len(extracted_pages),
                "preview": full_text[:500],
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