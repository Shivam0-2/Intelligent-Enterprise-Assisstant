from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "Intelligent Enterprise Assistant"
    debug: bool = True
    secret_key: str

    # Auth
    ALLOW_ANY_EMAIL: bool = True

    # Email
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    # Database
    database_url: str

    # JWT
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120

    # AI
    groq_api_key: str

    # Embeddings
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"

    # FAISS
    faiss_index_path: str = "./faiss_index"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()