from typing import List
import torch
from sentence_transformers import SentenceTransformer
from src.utils.logging import get_logger

logger = get_logger("Embeddings")

class LocalEmbedder:
    def __init__(self, model_path: str = r"C:\Users\Ayan\Projects\VisAgent\models\all-MiniLM-L6-v2"):
        device = "cpu"  # Force CPU
        logger.info(f"Loading embedder from {model_path} on {device}")
        self.model = SentenceTransformer(model_path, device=device)

    def embed_texts(self, texts: List[str], batch_size: int = 64) -> List[List[float]]:
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            emb = self.model.encode(
                batch,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            all_embeddings.extend(emb.tolist())
        return all_embeddings

    def embed_query(self, q: str) -> List[float]:
        return self.embed_texts([q])[0]
