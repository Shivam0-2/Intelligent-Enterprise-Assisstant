from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.utils.security import get_current_user, require_admin
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload/policy")
async def upload_policy_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Admin uploads a policy PDF.
    Pipeline: extract text → chunk → embed → store in FAISS + SQLite.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    result = await DocumentService.process_policy_document(
        file=file, uploader={"role": "admin"}, db=db
    )
    return {"message": "Policy document processed.", "details": result}


@router.post("/upload/personal")
async def upload_personal_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    result = await DocumentService.process_personal_document(file=file)

    return {
        "summary": result["summary"]
    }