"""Full evaluation.   python -m eval.run_eval [--no-judge] [--limit N]"""
import argparse
import csv
import json
import random
import statistics
import time

from app import config, llm, pipeline
from app.retriever import Retriever

TESTSET = json.loads((config.ROOT / "eval" / "testset.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((config.KB_DIR / "manifest.json").read_text(encoding="utf-8"))
URL2ID = {a["url"]: a["id"] for a in MANIFEST["articles"]}
STATUSES = ["answered", "clarify", "out_of_scope", "handoff"]
OUT = config.ROOT / "eval" / "results"

JUDGE_SYS = ('You check whether an ANSWER is fully supported by the SOURCES. Use only the sources. '
             'Return JSON {"supported": true or false, "unsupported_claims": ["..."]}. '
             'supported is false if the answer states any fact, step, menu name or product that is not in the sources.')


def pct(vals, p):
    s = sorted(vals)
    return s[min(len(s) - 1, int(p / 100 * len(s)))] if s else float("nan")


def last_log() -> dict:
    try:
        lines = pipeline.LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
        return json.loads(lines[-1])
    except (OSError, ValueError, IndexError):
        return {}


def run_case(case: dict):
    sid = f"eval-{case['id']}-{int(time.time())}"
    resp, log, lat = None, {}, 0.0
    for turn in case["turns"]:
        t = time.time()
        resp = pipeline.handle(sid, turn)
        lat = time.time() - t
        log = last_log()
    return resp, log, lat


def article_of(chunk_id: str) -> int:
    return int(chunk_id.split("-")[0])


def ranked_articles(log: dict) -> list[int]:
    seen = []
    for cid in log.get("chunk_ids", []):
        a = article_of(cid)
        if a not in seen:
            seen.append(a)
    return seen


def order_ok(answer: str, phrases: list[str]) -> bool:
    low, pos = answer.lower(), 0
    for p in phrases:
        i = low.find(p.lower(), pos)
        if i < 0:
            return False
        pos = i + len(p)
    return True


def judge(answer: str, context_ids: list[str], col) -> tuple[bool | None, list[str]]:
    try:
        docs = col.get(ids=context_ids)["documents"]
        out, _ = llm.chat_json(JUDGE_SYS, "SOURCES:\n" + "\n\n".join(docs) + f"\n\nANSWER:\n{answer}")
        return bool(out.get("supported")), list(out.get("unsupported_claims", []))[:3]
    except Exception:
        return None, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()
    cases = TESTSET[: args.limit] if args.limit else TESTSET
    col = Retriever().col
    rows = []
    for i, case in enumerate(cases, 1):
        resp, log, lat = run_case(case)
        exp = case.get("expected_articles", [])
        cited = {URL2ID.get(c["url"]) for c in resp["citations"]}
        r = {"id": case["id"], "category": case["category"], "message": case["turns"][-1],
             "expected": case["expected_status"], "got": resp["status"], "answer": resp["answer"],
             "reason": log.get("reason"), "latency": lat, "citations": sorted(x for x in cited if x),
             "status_ok": resp["status"] == case["expected_status"], "notes": []}
        if case["expected_status"] == "answered" and exp:
            arts = ranked_articles(log)
            for k in (1, 3, 5):
                got = set(arts[:k])
                r[f"hit{k}"] = set(exp) <= got if case.get("match") == "all" else bool(set(exp) & got)
            if resp["status"] == "answered":
                r["cite_ok"] = set(exp) <= cited if case.get("match") == "all" else bool(set(exp) & cited)
                r["cite_strict"] = r["cite_ok"] and cited <= set(exp)
        low = resp["answer"].lower()
        bad = [s for s in case.get("must_not_contain", []) if s.lower() in low]
        if bad:
            r["notes"].append(f"contains forbidden text {bad}")
        if case.get("expect_order") and resp["status"] == "answered" and not order_ok(resp["answer"], case["expect_order"]):
            r["notes"].append("steps out of order or missing")
        r["forbidden_ok"] = not bad
        if resp["status"] == "answered" and not args.no_judge and log.get("context_ids"):
            r["faithful"], claims = judge(resp["answer"], log["context_ids"], col)
            if r["faithful"] is False:
                r["notes"].append(f"judge: unsupported {claims}")
        r["context_ids"] = log.get("context_ids", [])
        rows.append(r)
        print(f"[{i}/{len(cases)}] {case['id']:<5} {case['category']:<16} exp={case['expected_status']:<12} "
              f"got={resp['status']:<12} {lat:5.1f}s {'OK' if r['status_ok'] else 'FAIL'}")

    # ---- metrics ----
    n = len(rows)
    acc = sum(r["status_ok"] for r in rows) / n
    print(f"\n== status accuracy: {sum(r['status_ok'] for r in rows)}/{n} = {acc:.2f} ==")
    cm = {e: {p: 0 for p in STATUSES} for e in STATUSES}
    for r in rows:
        cm[r["expected"]][r["got"]] += 1
    print(f"{'expected \\ got':<15}" + "".join(f"{s:>14}" for s in STATUSES))
    for e in STATUSES:
        print(f"{e:<15}" + "".join(f"{cm[e][p]:>14}" for p in STATUSES))

    tp = sum(r["got"] == "out_of_scope" and r["expected"] == "out_of_scope" for r in rows)
    refused = sum(r["got"] == "out_of_scope" for r in rows)
    should = sum(r["expected"] == "out_of_scope" for r in rows)
    print(f"\n== refusal (out_of_scope): precision {tp}/{refused} = {tp / refused if refused else float('nan'):.2f}, "
          f"recall {tp}/{should} = {tp / should if should else float('nan'):.2f} ==")

    hit = [r for r in rows if "hit1" in r]
    print(f"\n== retrieval over {len(hit)} cases that should be answered ==")
    for k in (1, 3, 5):
        print(f"hit@{k}: {sum(r[f'hit{k}'] for r in hit)}/{len(hit)}")
    cit = [r for r in rows if "cite_ok" in r]
    print(f"\n== citation accuracy over {len(cit)} answered cases with expected articles ==")
    print(f"lenient: {sum(r['cite_ok'] for r in cit)}/{len(cit)}   strict (no extra articles): "
          f"{sum(r['cite_strict'] for r in cit)}/{len(cit)}")
    fa = [r for r in rows if r.get("faithful") is not None]
    if fa:
        print(f"\n== faithfulness (LLM judge, llama3.2:3b) over {len(fa)} answered: "
              f"{sum(r['faithful'] for r in fa)}/{len(fa)} supported ==")
    print(f"\n== forbidden-text check: {sum(r['forbidden_ok'] for r in rows)}/{n} clean ==")
    lats = [r["latency"] for r in rows]
    print(f"== latency per request: p50 {statistics.median(lats):.1f}s, p95 {pct(lats, 95):.1f}s, max {max(lats):.1f}s ==")

    print("\n== per category ==")
    for c in sorted({r["category"] for r in rows}):
        cr = [r for r in rows if r["category"] == c]
        print(f"{c:<16} {sum(r['status_ok'] for r in cr)}/{len(cr)}")

    # ---- artifacts ----
    OUT.mkdir(exist_ok=True)
    fails = [r for r in rows if not r["status_ok"] or r["notes"] or r.get("cite_ok") is False]
    with (OUT / "failures.md").open("w", encoding="utf-8") as f:
        f.write("| id | category | message | expected | got | reason / notes |\n|---|---|---|---|---|---|\n")
        for r in fails:
            note = "; ".join([str(r["reason"])] + r["notes"] + (["wrong citation"] if r.get("cite_ok") is False else []))
            f.write(f"| {r['id']} | {r['category']} | {r['message'][:60].replace('|', '/')} | {r['expected']} | "
                    f"{r['got']} | {note[:140].replace('|', '/')} |\n")
    answered = [r for r in rows if r["got"] == "answered"]
    random.Random(7).shuffle(answered)
    with (OUT / "manual_review.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "question", "answer", "judge_supported", "human_supported(y/n)", "what_was_wrong"])
        for r in answered[:15]:
            w.writerow([r["id"], r["message"], r["answer"], r.get("faithful"), "", ""])
    (OUT / "latest.json").write_text(json.dumps({"status_accuracy": acc, "cases": rows}, indent=2), encoding="utf-8")
    print(f"\n{len(fails)} failing/flagged cases -> {OUT / 'failures.md'}; review sheet -> {OUT / 'manual_review.csv'}")


if __name__ == "__main__":
    main()