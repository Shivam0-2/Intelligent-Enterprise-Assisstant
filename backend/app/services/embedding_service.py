from sentence_transformers import SentenceTransformer
from app.config import get_settings

settings = get_settings()

# Model is loaded once when the module is first imported
model = None

def get_model():
    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer(settings.embedding_model)

    return model

class EmbeddingService:

    @staticmethod
    def embed_chunks(chunks: list[str]) -> list[list[float]]:
        """Takes a list of text chunks, returns a list of embedding vectors."""
        embeddings = get_model().encode(chunks, show_progress_bar=False)
        return embeddings.tolist()