"""python -m eval.debug_case t09"""
import json
import sys

from app import config, grounding
from app.generate import generate
from app.retriever import retrieve, select_context

cases = json.loads((config.ROOT / "eval" / "testset.json").read_text(encoding="utf-8"))
q = next(c for c in cases if c["id"] == sys.argv[1])["turns"][-1]


def logged_query(msg):
    try:
        for line in reversed((config.ROOT / "logs" / "requests.jsonl").read_text(encoding="utf-8").splitlines()):
            e = json.loads(line)
            if e["message"] == msg and e.get("rewritten_query"):
                return e["rewritten_query"]
    except OSError:
        pass
    return msg


query = logged_query(q)
ctx = select_context(query, retrieve(query, 12))
answer, used, _ = generate(query, ctx)


print("query:", query)
print("context:", [c["chunk_id"] for c in ctx])
print("raw answer:", answer)
print("support_ratio:", round(grounding.support_ratio(answer, ctx), 2), "(cutoff 0.60)")
kept, dropped = grounding.filter_supported(answer, ctx)
print("kept sentences:", kept, "| dropped:", dropped)