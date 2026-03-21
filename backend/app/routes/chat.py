from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.db import get_db
from app.utils.security import get_current_user
from app.utils.filters import contains_bad_words
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def handle_query(
    payload: QueryRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Main RAG query endpoint:
    1. Content moderation check
    2. Embed query → FAISS similarity search
    3. Feed retrieved context + query to LLM
    4. Return generated answer
    """
    if contains_bad_words(payload.query):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your query contains inappropriate language.",
        )

    answer = ChatService.process_query(query=payload.query, user=current_user)
    return {"query": payload.query, "answer": answer}