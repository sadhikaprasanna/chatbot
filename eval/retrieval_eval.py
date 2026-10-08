"""Retrieval-only evaluation (no LLM).   python -m eval.retrieval_eval"""
import json
import statistics

from app import config
from app.retriever import Retriever

TESTSET = json.loads((config.ROOT / "eval" / "testset.json").read_text(encoding="utf-8"))
IN_SCOPE = {"single_article", "multi_step", "messy", "two_articles", "partial",
            "false_premise", "action_request"}
SHOULD_REFUSE = {"oos_general", "oos_near_miss"}
K_MAX = 10


def pct(values, p):
    s = sorted(values)
    return s[min(len(s) - 1, int(p / 100 * len(s)))] if s else float("nan")


def summary(name, scores):
    if not scores:
        return
    print(f"{name:<22} n={len(scores):<3} min={min(scores):.3f} p25={pct(scores,25):.3f} "
          f"median={statistics.median(scores):.3f} p75={pct(scores,75):.3f} max={max(scores):.3f}")


def main():
    r = Retriever()
    rows = []
    for case in TESTSET:
        if len(case["turns"]) != 1:
            continue                                  # multi-turn needs query rewriting
        hits = r.retrieve(case["turns"][0], K_MAX)
        arts = []
        for h in hits:
            if h["article_id"] not in arts:
                arts.append(h["article_id"])
        rows.append({"id": case["id"], "cat": case["category"], "q": case["turns"][0],
                     "top1": hits[0]["score"], "margin": hits[0]["score"] - hits[min(4, len(hits)-1)]["score"],
                     "arts": arts, "exp": case.get("expected_articles", []),
                     "match": case.get("match", "any"),
                     "top_title": hits[0]["title"][:30]})

    # ---- hit@k on in-scope cases ----
    ins = [x for x in rows if x["cat"] in IN_SCOPE]
    print(f"\n== hit@k over {len(ins)} in-scope single-turn cases ==")
    for k in (1, 3, 5):
        ok = 0
        for x in ins:
            got = set(x["arts"][:k])
            ok += set(x["exp"]) <= got if x["match"] == "all" else bool(set(x["exp"]) & got)
        print(f"hit@{k}: {ok}/{len(ins)} = {ok/len(ins):.2f}")
    print("misses at k=5:")
    for x in ins:
        got = set(x["arts"][:5])
        good = set(x["exp"]) <= got if x["match"] == "all" else bool(set(x["exp"]) & got)
        if not good:
            print(f"  {x['id']} {x['q'][:60]!r} expected {x['exp']} got {x['arts'][:5]}")

    # ---- score distributions ----
    print("\n== top-1 score distribution ==")
    groups = {"in-scope": [x["top1"] for x in ins]}
    for c in sorted(SHOULD_REFUSE):
        groups[c] = [x["top1"] for x in rows if x["cat"] == c]
    for name, vals in groups.items():
        summary(name, vals)
    print("\nlowest 5 in-scope scores (these decide how high the threshold can go):")
    for x in sorted(ins, key=lambda x: x["top1"])[:5]:
        print(f"  {x['top1']:.3f} {x['id']} {x['q'][:60]!r}")
    print("\nshould-refuse scores:")
    for x in sorted((x for x in rows if x["cat"] in SHOULD_REFUSE), key=lambda x: -x["top1"]):
        print(f"  {x['top1']:.3f} {x['id']} [{x['cat']}] {x['q'][:50]!r} -> {x['top_title']}")

    # ---- threshold sweep: refuse if top1 < t ----
    ref = [x for x in rows if x["cat"] in SHOULD_REFUSE]
    print("\n== threshold sweep (positive = should refuse) ==")
    print(f"{'t':>5} {'TP':>3} {'FP':>3} {'FN':>3} {'precision':>9} {'recall':>6} {'in-scope wrongly refused':>25}")
    t = 0.10
    while t <= 0.60:
        tp = sum(x["top1"] < t for x in ref)
        fn = len(ref) - tp
        fp = sum(x["top1"] < t for x in ins)
        prec = tp / (tp + fp) if tp + fp else float("nan")
        rec = tp / len(ref) if ref else float("nan")
        print(f"{t:>5.2f} {tp:>3} {fp:>3} {fn:>3} {prec:>9.2f} {rec:>6.2f} {fp:>14}/{len(ins)}")
        t = round(t + 0.05, 2)

    # ---- other categories, for information ----
    print("\n== other categories (information only) ==")
    for c in ("confusable", "ambiguous", "handoff", "prompt_injection"):
        vals = [x["top1"] for x in rows if x["cat"] == c]
        summary(c, vals)

    out = config.ROOT / "eval" / "results"
    out.mkdir(exist_ok=True)
    (out / "retrieval_scores.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"\nsaved per-case scores to {out / 'retrieval_scores.json'}")


if __name__ == "__main__":
    main()