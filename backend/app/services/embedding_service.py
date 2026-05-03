from sentence_transformers import SentenceTransformer
from app.config import get_settings

settings = get_settings()

# Model is loaded once when the module is first imported
_model = SentenceTransformer(settings.embedding_model)


class EmbeddingService:

    @staticmethod
    def embed_chunks(chunks: list[str]) -> list[list[float]]:
        """Takes a list of text chunks, returns a list of embedding vectors."""
        embeddings = _model.encode(chunks, show_progress_bar=False)
        return embeddings.tolist()