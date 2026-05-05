import resend
import random

from app.config import get_settings
settings = get_settings()
resend.api_key = settings.resend_api
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt
from fastapi import HTTPException


# TEMP in-memory store (for now)
otp_store = {}
user_store = {}

#ADMIN EMAILS - In a real application, this would come from a database or config file 
ADMIN_EMAILS = [
    "admin@company.com",
    "hr@company.com",
    "manager@company.com",
    "shivamkale5092@gmail.com"
]


class AuthService:

    @staticmethod
    def send_otp(email: str, db: Session) -> None:

        # COMPANY EMAIL RESTRICTION
        
        if not settings.ALLOW_ANY_EMAIL:
            if not email.endswith("@company.com"):
                raise HTTPException(
                status_code=400,
                detail="Only company email IDs are allowed"
            )

        otp = str(random.randint(100000, 999999))

        otp_store[email] = {
            "otp": otp,
            "expires": datetime.utcnow() + timedelta(minutes=5)
        }

        #ADMIN ROLE LOGIC
        role = "admin" if email in ADMIN_EMAILS else "user"

        user_store[email] = {
            "email": email,
            "role": role
        }

        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": email,
                "subject": "Your OTP Code",
                "html": f"""
                    <h2>Your OTP Code</h2>
                    <p>Your OTP is: <strong>{otp}</strong></p>
                    <p>This will expire in 10 minutes.</p>
                """
            })
        except Exception as e:
            print("Resend error:", str(e))
            raise Exception("Failed to send OTP email")


    @staticmethod
    def verify_otp(email: str, otp: str, db: Session):

        record = otp_store.get(email)

        if not record:
            raise HTTPException(status_code=400, detail="OTP not found")

        if datetime.utcnow() > record["expires"]:
            raise HTTPException(status_code=400, detail="OTP expired")

        if record["otp"] != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        user = user_store.get(email)

        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        token_data = {
            "sub": email,
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=2)
        }

        token = jwt.encode(
            token_data,
            settings.secret_key,
            algorithm=settings.jwt_algorithm
        )

        return {
            "access_token": token,
            "role": user["role"]
        }