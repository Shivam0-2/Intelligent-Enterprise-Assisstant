from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database.db import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Request schemas ──────────────────────────────────────────────────────────

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/request-otp", status_code=status.HTTP_200_OK)
def request_otp(payload: OTPRequest, db: Session = Depends(get_db)):
    """
    Step 1 of login: registers the user (if new) and sends a 6-digit OTP
    to their email address.
    """
    AuthService.send_otp(email=payload.email, db=db)
    return {"message": "OTP sent successfully. Check your email."}


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(payload: OTPVerify, db: Session = Depends(get_db)):
    """
    Step 2 of login: validates the OTP and returns a signed JWT on success.
    """
    token = AuthService.verify_otp(email=payload.email, otp=payload.otp, db=db)
    return {"access_token": token, "token_type": "bearer"}