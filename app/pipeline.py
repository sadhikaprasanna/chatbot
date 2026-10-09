"""The request path: message -> response dict matching the /chat contract."""
import json
import time
from datetime import datetime, timezone

from app import config, gate, grounding, rewrite, safety, sessions
from app.generate import generate
from app.llm import LLMError
from app.retriever import retrieve, select_context
FETCH_K = 12
SUPPORT_MIN = float(__import__("os").getenv("SUPPORT_MIN", "0.60"))
FALLBACK = "Sorry, something went wrong on my side. Please try again in a moment."
NO_GROUND = ("I couldn't find a reliable answer to that in our help articles, so I'd rather not guess. "
             "Could you rephrase, or would you like me to hand you to a person?")
ACTION_NOTE = ("I can't perform actions like cancelling or refunding for you, but the help article above "
               "explains the steps you can follow yourself.")
LOG_FILE = config.ROOT / "logs" / "requests.jsonl"


def _response(status, answer, citations=None, handoff=None):
    return {"status": status, "answer": answer, "citations": citations or [], "handoff": handoff}


def _citations(chunks: list[dict], used_ids: list[str]) -> list[dict]:
    seen, out = set(), []
    for c in chunks:
        if c["chunk_id"] in used_ids:
            key = (c["url"], c["section"])
            if key not in seen:
                seen.add(key)
                out.append({"title": c["title"], "url": c["url"], "section": c["section"]})
    return out


def _handoff(session, intent: str, why: str):
    summary = (f"User issue: {session.last_user_issue or 'unclear'}. "
               f"Bot could not resolve it ({why}) after {session.failures} attempt(s).")
    return _response("handoff",
                     "I'm sorry I couldn't resolve this. I'm passing you to a human agent with a summary "
                     "so you won't have to repeat yourself.",
                     handoff={"summary": summary, "intent": intent,
                              "articles_tried": list(session.articles_tried)})


def _log(entry: dict) -> None:
    try:
        LOG_FILE.parent.mkdir(exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def handle(session_id: str, message: str) -> dict:
    t0 = time.time()
    s = sessions.get_session(session_id)
    log = {"ts": datetime.now(timezone.utc).isoformat(), "session": session_id, "message": message,
           "chunk_ids": [], "scores": [], "tokens": {"prompt": 0, "completion": 0}}
    try:
        resp = _run(s, message, log)
    except Exception as exc:                       # never leak a stack trace to the client
        log["error"] = f"{type(exc).__name__}: {exc}"
        resp = _response("out_of_scope", FALLBACK)
    s.add_user(message)
    s.add_assistant(resp["answer"][:500])
    log.update(status=resp["status"], reason=log.get("reason"), latency_s=round(time.time() - t0, 2))
    _log(log)
    return resp


def _run(s, message: str, log: dict) -> dict:
    # 1. explicit request for a person
    if safety.wants_human(message):
        log["reason"] = "user_asked_for_human"
        return _handoff(s, "human_requested", "user asked for a person")

    # 2. injection: strip the attack, keep a real question if one remains
    clean = message
    if safety.is_injection(message):
        clean = safety.strip_injection(message)
        log["injection"] = True
        if not clean:
            log["reason"] = "injection_only"
            s.record("out_of_scope")
            return _after_failure(s, "out_of_scope", gate.OUT_OF_SCOPE_MSG, "prompt_injection")

    # 3. resolve follow-ups
    query, u1 = rewrite.rewrite(s.history, clean)
    log["rewritten_query"] = query

    # 4. retrieve (retrieve on the rewritten query)
    chunks = retrieve(query, FETCH_K)                 # was config.TOP_K
    log["chunk_ids"] = [c["chunk_id"] for c in chunks]
    log["scores"] = [round(c["score"], 3) for c in chunks]
    s.last_user_issue = clean[:200]

    # 5. gate (vague check on the original text, scope guard on both)
    d = gate.decide(query if s.history else clean, chunks)
    log["reason"] = d.reason
    if d.action != "proceed":
        s.record(d.action)
        return _after_failure(s, d.action, d.message, d.reason)


    # 6. generate + ground

    ctx = select_context(query, chunks)
    log["context_ids"] = [c["chunk_id"] for c in ctx]
    try:
        answer, used, u2 = generate(query, ctx)       # was chunks

    
    except LLMError as exc:
        log["error"] = str(exc)
        return _response("out_of_scope", FALLBACK)
    log["tokens"] = {"prompt": u1["prompt_tokens"] + u2["prompt_tokens"],
                     "completion": u1["completion_tokens"] + u2["completion_tokens"]}
    ratio = grounding.support_ratio(answer, ctx)
    log["support_ratio"] = round(ratio, 2)
    if not answer or not used or ratio < SUPPORT_MIN:
        log["reason"] = "ungrounded"
        s.record("out_of_scope")
        return _after_failure(s, "out_of_scope", NO_GROUND, "ungrounded")
    cites = _citations(ctx, used)
    if grounding.claims_action(answer):
        answer = ACTION_NOTE
        log["reason"] = "action_claim_replaced"
    s.record("answered", [c["url"] for c in cites])
    return _response("answered", answer, cites)


def _after_failure(s, status: str, message: str, why: str) -> dict:
    if s.failures >= 2:
        return _handoff(s, why, why)
    return _response(status, message)