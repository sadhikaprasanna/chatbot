"""Rule-based checks that run before any retrieval or LLM call."""
import re

INJECTION_PATTERNS = [
    r"ignore (all |your |the |any )?(previous |prior |above )?(rules|instructions|prompts?)",
    r"disregard (all |your |the |any )?(previous |prior |above )?(rules|instructions|prompts?|above)",
    r"(reveal|print|show|display|repeat|tell me) (me )?(your |the )?(system |hidden |initial )?(prompt|instructions)",
    r"system prompt",
    r"you are now\b",
    r"\bdan\b",
    r"developer mode",
    r"pretend (to be|you are)",
    r"act as (a |an )?(?!firefox)",
    r"jailbreak",
    r"forget (everything|your|all)",
]
HANDOFF_PATTERNS = [
    r"(talk|speak|chat) (to|with) (a |an |the )?(real |live )?(person|human|agent|representative|someone)",
    r"(human|live|real) (agent|person|being|support)",
    r"\b(customer service|support) (agent|rep|representative)\b",
    r"connect me (to|with)",
    r"\bescalate\b",
]
_INJ = [re.compile(p, re.I) for p in INJECTION_PATTERNS]
_HAND = [re.compile(p, re.I) for p in HANDOFF_PATTERNS]
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def is_injection(text: str) -> bool:
    return any(p.search(text) for p in _INJ)


def wants_human(text: str) -> bool:
    return any(p.search(text) for p in _HAND)


def strip_injection(text: str) -> str:
    """Drop sentences that contain an attack; return what is left (may be empty)."""
    kept = [s for s in _SENT_SPLIT.split(text.strip()) if not is_injection(s)]
    return " ".join(kept).strip()