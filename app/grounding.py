"""Code-level grounding and action checks (no LLM)."""
import re

STOP = set("the a an and or of to in on for with is are be it you your this that can will if at as by from "
           "not do does how what when which then also so but use using click select open go any more "
           "there their they we our have has may should would could its into out up".split())
ACTION_CLAIMS = re.compile(
    r"\b(i('| ha)?ve|i have|i)\s+(just\s+)?(cancel+ed|refunded|uninstalled|deleted|removed|issued|processed|reset)\b|"
    r"\b(has|have) been (cancel+ed|refunded|uninstalled|processed|issued)\b|"
    r"\bi('ll| will) (cancel|refund|uninstall) (it|your)\b", re.I)


def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z\-']{3,}", text.lower()) if w not in STOP}


def support_ratio(answer: str, chunks: list[dict]) -> float:
    """Share of the answer's content words that appear in the retrieved text."""
    answer = re.sub(r"\[\d+\]|\bsources?\b", "", answer, flags=re.I)
    words = content_words(answer)
    if not words:
        return 0.0
    source = content_words(" ".join(c["text"] for c in chunks))
    return len(words & source) / len(words)


def claims_action(answer: str) -> bool:
    return bool(ACTION_CLAIMS.search(answer))

def filter_supported(answer: str, chunks: list[dict], min_ratio: float = 0.5):
    """Drop sentences whose content words are mostly absent from the sources."""
    parts = [s.strip() for s in re.split(r"(?<=[a-z\)][.!?])\s+|\n+", answer) if s.strip()]
    kept = [s for s in parts if not content_words(s) or support_ratio(s, chunks) >= min_ratio]
    return kept, len(kept) < len(parts)