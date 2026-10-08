from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app import config


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(config.EMBED_MODEL)


def embed(texts: list[str]) -> list[list[float]]:
    """L2-normalised vectors, so cosine similarity = dot product."""
    return get_model().encode(texts, normalize_embeddings=True, batch_size=32,
                              show_progress_bar=False).tolist()