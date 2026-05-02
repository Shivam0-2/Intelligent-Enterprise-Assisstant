import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt

from app.config import get_settings

settings = get_settings()

# TEMP in-memory store (for now)
otp_store = {}
user_store = {}


class AuthService:

    @staticmethod
    def send_otp(email: str, db: Session) -> None:
        otp = str(random.randint(100000, 999999))

        otp_store[email] = {
            "otp": otp,
            "expires": datetime.utcnow() + timedelta(minutes=5)
        }

        # Assign role (VERY IMPORTANT for your project)
        if email.endswith("@admin.com"):
            role = "admin"
        else:
            role = "user"

        user_store[email] = {
            "email": email,
            "role": role
        }

        print(f"OTP for {email}: {otp}")  # for demo


    @staticmethod
    def verify_otp(email: str, otp: str, db: Session):
        record = otp_store.get(email)

        if not record:
            raise Exception("OTP not found")

        if datetime.utcnow() > record["expires"]:
            raise Exception("OTP expired")

        if record["otp"] != otp:
            raise Exception("Invalid OTP")

        user = user_store.get(email)

        token_data = {
            "sub": email,
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=2)
        }

        token = jwt.encode(token_data, settings.secret_key, algorithm=settings.jwt_algorithm)

        return {
            "access_token": token,
            "role": user["role"]
        }