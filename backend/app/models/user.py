from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="employee")          # "employee" | "admin"
    is_verified = Column(Boolean, default=False)
    otp_code = Column(String, nullable=True)           # Stored temporarily during login
    otp_expires_at = Column(DateTime, nullable=True)   # OTP expiry timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())