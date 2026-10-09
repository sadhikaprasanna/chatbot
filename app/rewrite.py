"""Resolve follow-ups using conversation history."""
from app import llm

SYSTEM = (
    "You rewrite the user's latest message into one standalone search query, using the conversation "
    "for context. Keep product names and operating systems. Do not answer the question. "
    'Return JSON: {"query": "<standalone query>"}'
)


def rewrite(history: list[dict], message: str) -> tuple[str, dict]:
    if not history:
        return message, {"prompt_tokens": 0, "completion_tokens": 0}
    convo = "\n".join(f"{h['role']}: {h['content'][:300]}" for h in history[-6:])
    user = f"Conversation:\n{convo}\n\nLatest message: {message}\n\nStandalone query:"
    try:
        out, usage = llm.chat_json(SYSTEM, user)
        q = str(out.get("query", "")).strip()
        return (q if 3 <= len(q) <= 300 else message), usage
    except llm.LLMError:
        return message, {"prompt_tokens": 0, "completion_tokens": 0}