"""Retrieval without any LLM.   python -m app.retriever "how do I clear my cache?" """
import sys
from functools import lru_cache

import chromadb

from app import config
from app.embedder import embed


class Retriever:
    def __init__(self, client=None, name=None):
        client = client or chromadb.PersistentClient(path=str(config.CHROMA_DIR))
        self.col = client.get_collection(name or config.COLLECTION)

    def retrieve(self, query: str, k: int | None = None) -> list[dict]:
        k = k or config.TOP_K
        res = self.col.query(query_embeddings=embed([query]), n_results=k,
                             include=["documents", "metadatas", "distances"])
        out = []
        for cid, doc, meta, dist in zip(res["ids"][0], res["documents"][0],
                                        res["metadatas"][0], res["distances"][0]):
            out.append({"chunk_id": cid, "text": doc, "score": 1.0 - dist, **meta})
        return out


@lru_cache(maxsize=1)
def _default() -> Retriever:
    return Retriever()


def retrieve(query: str, k: int | None = None) -> list[dict]:
    return _default().retrieve(query, k)


if __name__ == "__main__":
    for r in retrieve(" ".join(sys.argv[1:]) or "how do I refresh Firefox?"):
        print(f"{r['score']:.3f}  {r['chunk_id']}  {r['title'][:40]} > {r['section'][:40]}")