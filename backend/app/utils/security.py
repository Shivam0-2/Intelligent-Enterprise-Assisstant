from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import get_settings

settings = get_settings()
bearer_scheme = HTTPBearer()


def create_access_token(data: dict) -> str:
    """Create a signed JWT from a payload dict."""
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT. Raises HTTPException on failure."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    FastAPI dependency — extracts & validates the Bearer token from
    the Authorization header, returning the decoded payload.
    Usage:  current_user: dict = Depends(get_current_user)
    """
    return decode_access_token(credentials.credentials)


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency that additionally checks the user holds the 'admin' role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user