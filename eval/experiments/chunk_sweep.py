"""Chunk size x overlap sweep.   python -m eval.experiments.chunk_sweep"""
import json

import chromadb

from app import config
from app.chunker import wc
from app.embedder import get_model
from app.index import build_index
from app.retriever import Retriever

PROBE = json.loads((config.ROOT / "eval" / "probe.json").read_text(encoding="utf-8"))
SIZES, OVERLAPS, K_MAX = [80, 120, 150, 200, 300], [0, 30, 60], 5


def run(size: int, overlap: int) -> dict:
    client = chromadb.EphemeralClient()
    name = f"sweep_{size}_{overlap}"
    chunks = build_index(size, overlap, client=client, name=name)
    r = Retriever(client, name)
    tok, limit = get_model().tokenizer, get_model().max_seq_length
    over = sum(len(tok(c.text)["input_ids"]) > limit for c in chunks)
    hits = {1: 0, 3: 0, 5: 0}
    rr = 0.0
    for p in PROBE:
        arts = []
        for x in r.retrieve(p["q"], K_MAX):               # article ids by rank, de-duplicated
            if x["article_id"] not in arts:
                arts.append(x["article_id"])
        for k in hits:
            hits[k] += any(a in p["expected"] for a in arts[:k])
        rank = next((i + 1 for i, a in enumerate(arts) if a in p["expected"]), None)
        rr += 1 / rank if rank else 0
    n = len(PROBE)
    return {"size": size, "ov": overlap, "chunks": len(chunks),
            "avg_words": sum(wc(c.body) for c in chunks) // len(chunks),
            "pct_trunc": 100 * over / len(chunks),
            "h1": hits[1] / n, "h3": hits[3] / n, "h5": hits[5] / n, "mrr": rr / n}


if __name__ == "__main__":
    print(f"{'size':>4} {'ov':>3} {'chunks':>6} {'avg_w':>5} {'>256tok%':>8} {'hit@1':>6} {'hit@3':>6} {'hit@5':>6} {'MRR':>5}")
    for s in SIZES:
        for o in OVERLAPS:
            if o >= s // 2:
                continue
            m = run(s, o)
            print(f"{m['size']:>4} {m['ov']:>3} {m['chunks']:>6} {m['avg_words']:>5} {m['pct_trunc']:>8.1f} "
                  f"{m['h1']:>6.2f} {m['h3']:>6.2f} {m['h5']:>6.2f} {m['mrr']:>5.2f}")