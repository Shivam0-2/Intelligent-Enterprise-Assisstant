"""
AuthService — handles OTP generation, email dispatch, and JWT issuance.
Implementation will be added in the Authentication step.
"""
from sqlalchemy.orm import Session


class AuthService:

    @staticmethod
    def send_otp(email: str, db: Session) -> None:
        """
        1. Create/fetch user record in DB
        2. Generate a 6-digit OTP with expiry
        3. Persist OTP hash to DB
        4. Send OTP via SMTP
        """
        raise NotImplementedError("AuthService.send_otp — coming in Step 2")

    @staticmethod
    def verify_otp(email: str, otp: str, db: Session) -> str:
        """
        1. Fetch user from DB
        2. Compare OTP + check expiry
        3. Mark user as verified
        4. Return signed JWT
        """
        raise NotImplementedError("AuthService.verify_otp — coming in Step 2")