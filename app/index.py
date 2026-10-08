"""Rebuild the vector index.   python -m app.index [--chunk-words N] [--overlap N]"""
import argparse
import time

import chromadb

from app import config
from app.chunker import chunk_all, wc
from app.embedder import embed


def build_index(chunk_words=None, overlap=None, client=None, name=None):
    chunks = chunk_all(chunk_words, overlap)
    client = client or chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    name = name or config.COLLECTION
    try:
        client.delete_collection(name)            # makes the rebuild idempotent
    except Exception:
        pass
    col = client.create_collection(name, metadata={"hnsw:space": "cosine"})
    vectors = embed([c.text for c in chunks])
    for i in range(0, len(chunks), 128):
        batch = chunks[i:i + 128]
        col.add(
            ids=[c.chunk_id for c in batch],
            documents=[c.text for c in batch],
            embeddings=vectors[i:i + 128],
            metadatas=[{"article_id": c.article_id, "title": c.title, "url": c.url,
                        "product": c.product, "section": c.section, "index": c.index}
                       for c in batch],
        )
    return chunks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk-words", type=int)
    ap.add_argument("--overlap", type=int)
    a = ap.parse_args()
    t = time.time()
    chunks = build_index(a.chunk_words, a.overlap)
    print(f"Indexed {len(chunks)} chunks (avg {sum(wc(c.body) for c in chunks)//len(chunks)} words) "
          f"into '{config.COLLECTION}' in {time.time()-t:.1f}s")