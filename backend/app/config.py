from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "IntelligentEnterpriseAssistant"
    debug: bool = True
    secret_key: str

    # Database
    database_url: str = "sqlite:///./enterprise_assistant.db"

    # JWT
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Email / SMTP
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str

    # LLM
    hf_api_token: str
    llm_model: str = "mistralai/Mistral-7B-Instruct-v0.1"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # FAISS
    faiss_index_path: str = "./faiss_index"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Cache settings so .env is only read once."""
    return Settings()