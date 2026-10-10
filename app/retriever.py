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

import re

STEP_Q = re.compile(r"\b(how (do|can|could|should|to)|steps?|walk me through|instructions?)\b", re.I)
HAS_STEPS = re.compile(r"^\s*\d+\.\s", re.M)

def select_context(query: str, hits: list[dict], max_chunks: int = 4,
                   budget_words: int = 400, step_boost: float = 0.15,
                   article_margin: float = 0.05) -> list[dict]:
    """Choose the chunks sent to the LLM. Raw scores are untouched (the gate uses them)."""
    if not hits:
        return []
    procedural = bool(STEP_Q.search(query))

    # keep only articles whose best raw score is close to the overall best
    best = max(h["score"] for h in hits)
    art_best = {}
    for h in hits:
        art_best[h["article_id"]] = max(art_best.get(h["article_id"], 0.0), h["score"])
    keep = {a for a, s in art_best.items() if s >= best - article_margin}
    hits = [h for h in hits if h["article_id"] in keep]

    def adj(h):
        return h["score"] + (step_boost if procedural and HAS_STEPS.search(h["text"]) else 0.0)

    chosen, words = [], 0
    for h in sorted(hits, key=adj, reverse=True):
        w = len(h["text"].split())
        if chosen and words + w > budget_words:
            continue
        chosen.append(h)
        words += w
        if len(chosen) == max_chunks:
            break
    order = {}
    for h in chosen:
        order.setdefault(h["article_id"], len(order))
    return sorted(chosen, key=lambda h: (order[h["article_id"]], h["index"]))


if __name__ == "__main__":
    for r in retrieve(" ".join(sys.argv[1:]) or "how do I refresh Firefox?"):
        print(f"{r['score']:.3f}  {r['chunk_id']}  {r['title'][:40]} > {r['section'][:40]}")