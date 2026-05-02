from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database.db import get_db
from app.utils.security import get_current_user
from app.utils.filters import contains_bad_words
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = None   # ✅ ADD THIS


@router.post("/query")
def handle_query(
    payload: QueryRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Main RAG query endpoint
    """

    if contains_bad_words(payload.query):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your query contains inappropriate language.",
        )

    result = ChatService.process_query(
        query=payload.query,
        user=current_user,
        context=payload.context   # ✅ PASS CONTEXT
    )

    return result   # ✅ FIX DOUBLE NESTING