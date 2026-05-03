from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "Intelligent EnterpriseAssistant"
    debug: bool = True
    secret_key: str

    ALLOW_ANY_EMAIL: bool = True
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    hf_api_token: str | None = None
    groq_api_key: str | None = None

    class Config:
        env_file = ".env"

    # Database
    database_url: str = "sqlite:///./enterprise_assistant.db"

    # JWT
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Email / SMTP
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    llm_model: str = "mistralai/Mistral-7B-Instruct-v0.1"

    # Embeddings
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"

    # FAISS
    faiss_index_path: str = "./faiss_index"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Cache settings so .env is only read once."""
    return Settings()