"""Decides whether to answer, clarify or refuse. No LLM involved."""
import re
from dataclasses import dataclass

from app import config

FOREIGN = [
    "chrome", "chromium", "safari", "edge", "opera", "brave", "vivaldi", "internet explorer",
    "nordvpn", "expressvpn", "surfshark", "mullvad", "cyberghost", "windscribe", "tunnelbear",
    "firefox for android", "firefox for ios", "firefox android", "firefox ios",
    "thunderbird", "firefox focus", "firefox relay",
]
_FOREIGN_RE = re.compile(r"\b(" + "|".join(re.escape(f) for f in FOREIGN) + r")\b", re.I)
_FIREFOX_RE = re.compile(r"\b(firefox|ff)\b", re.I)
_MOBILE_FX_RE = re.compile(r"\bfirefox (for )?(android|ios|focus|relay)\b|\bfirefox (android|ios)\b", re.I)

VAGUE_EXACT = {"help", "hi", "hello", "hey", "hii", "test", "?", "ok", "okay"}
VAGUE_PATTERNS = [
    r"^(it|this|that|everything)('?s| is| isn'?t| is not| does ?n'?t| doesn'?t| won'?t)? ?(not )?(working|work|broken|fixed)\b",
    r"^(it'?s|it is) (broken|not working|not right|weird)",
    r"^(how|what) (do|can|should) i (clear|fix|reset|remove|delete|turn off|disable|update) (it|this|that)\??$",
    r"^(fix|help) (it|this|me)\b",
    r"^(something|stuff) (is )?(wrong|broken|not working)",
]
_VAGUE = [re.compile(p, re.I) for p in VAGUE_PATTERNS]
_VPN_RE = re.compile(r"\bvpn\b", re.I)
_PRODUCT_NAMED_RE = re.compile(r"\b(mozilla vpn|proton ?vpn|mozillavpn)\b", re.I)
_REFUND_RE = re.compile(r"\b(refund|money back|cancel|subscription|billing|charge)\b", re.I)
_CLEAR_STORED_RE = re.compile(r"\b(clear|delete|remove) (stored |saved |my )?(data|browsing data|site data)\b", re.I)
_CACHE_OR_COOKIE_RE = re.compile(r"\b(cache|cookies?)\b", re.I)


@dataclass
class Decision:
    action: str            # "proceed" | "clarify" | "out_of_scope"
    reason: str
    message: str = ""      # text to show the user when not proceeding

_VAGUE_SHORT = re.compile(r"^(it|this|that|everything)\b.*\b(not working|isn'?t working|doesn'?t work|does not work|broken|not right)\b", re.I)

def is_vague(text: str) -> bool:
    t = text.strip().lower().rstrip("!.?")
    if t in VAGUE_EXACT or len(t) < 3:
        return True
    if len(t.split()) <= 6 and _VAGUE_SHORT.search(t):
        return True
    return any(p.search(t) for p in _VAGUE)


def mentions_foreign_product(text: str) -> bool:
    if _MOBILE_FX_RE.search(text):
        return True
    m = _FOREIGN_RE.search(text)
    if not m:
        return False
    return not _FIREFOX_RE.search(text)        # "chrome works but ff doesn't" stays in scope


def needs_product_clarification(text: str, retrieved: list[dict]) -> str | None:
    """Return a clarifying question, or None."""
    products = {r["product"] for r in retrieved[:3]}
    if _VPN_RE.search(text) and _REFUND_RE.search(text) and not _PRODUCT_NAMED_RE.search(text):
        if {"mozilla-vpn", "proton-vpn"} <= products:
            return "Which VPN is this about: Mozilla VPN or ProtonVPN?"
    if _CLEAR_STORED_RE.search(text) and not _CACHE_OR_COOKIE_RE.search(text):
        return "Do you want to clear cookies and site data, or the cache?"
    return None


def decide(text: str, retrieved: list[dict], threshold: float | None = None) -> Decision:
    threshold = config.SCORE_THRESHOLD if threshold is None else threshold
    if is_vague(text):
        return Decision("clarify", "vague",
                        "Could you tell me a bit more? For example, what are you trying to do in Firefox, "
                        "and what happens when you try?")
    if mentions_foreign_product(text):
        return Decision("out_of_scope", "foreign_product", OUT_OF_SCOPE_MSG)
    if not retrieved or retrieved[0]["score"] < threshold:
        return Decision("out_of_scope", "low_score", OUT_OF_SCOPE_MSG)
    q = needs_product_clarification(text, retrieved)
    if q:
        return Decision("clarify", "ambiguous_product", q)
    return Decision("proceed", "ok")


OUT_OF_SCOPE_MSG = ("I can only help with Firefox and the Mozilla VPN / ProtonVPN offering covered in our "
                    "help articles, and I couldn't find that there. I can help with things like refreshing "
                    "Firefox, clearing the cache or cookies, updating, bookmarks, add-ons, Sync, "
                    "Private Browsing, or VPN refunds.")