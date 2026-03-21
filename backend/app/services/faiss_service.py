import os
import json
import numpy as np
import faiss
from app.config import get_settings

settings = get_settings()

INDEX_PATH = settings.faiss_index_path + "/index.faiss"
CHUNKS_PATH = settings.faiss_index_path + "/chunks.json"


class FaissService:

    @staticmethod
    def create_index(dim: int) -> faiss.IndexFlatL2:
        """Creates a new flat L2 index for vectors of size `dim`."""
        return faiss.IndexFlatL2(dim)

    @staticmethod
    def add_embeddings(
        index: faiss.IndexFlatL2,
        embeddings: list[list[float]],
        chunks: list[str],
    ) -> dict:
        """
        Adds embedding vectors to the index.
        Also saves chunk texts mapped by their index position.
        Returns updated total vector count.
        """
        vectors = np.array(embeddings, dtype=np.float32)

        if vectors.shape[1] != index.d:
            raise ValueError(
                f"Embedding dimension {vectors.shape[1]} does not match index dimension {index.d}"
            )
        index.add(vectors)

        # Load existing chunk map if present, then append
        if os.path.exists(CHUNKS_PATH):
            with open(CHUNKS_PATH, "r") as f:
                chunk_map = json.load(f)
        else:
            chunk_map = {}

        offset = len(chunk_map)
        for i, chunk in enumerate(chunks):
            chunk_map[str(offset + i)] = chunk

        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        with open(CHUNKS_PATH, "w") as f:
            json.dump(chunk_map, f)

        return {"total_vectors": index.ntotal}

    @staticmethod
    def save_index(index: faiss.IndexFlatL2) -> None:
        """Saves the FAISS index to disk."""
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        faiss.write_index(index, INDEX_PATH)

    @staticmethod
    def load_index() -> faiss.IndexFlatL2:
        """Loads the FAISS index from disk. Raises errors if directory or file not found."""
        index_dir = os.path.dirname(INDEX_PATH)
        if not os.path.exists(index_dir):
            raise FileNotFoundError(f"FAISS index directory not found: {index_dir}")
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"No FAISS index found at {INDEX_PATH}")
        return faiss.read_index(INDEX_PATH)