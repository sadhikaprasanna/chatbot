"""Heading-aware chunker.

python -m app.chunker              # stats per article
python -m app.chunker --show 17    # print the chunks of article 17
"""
import argparse
import json
import re
from dataclasses import dataclass

from app import config

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_ITEM_RE = re.compile(r"^(\d+\.|[-*+])\s+")
PRODUCT_LABEL = {"firefox": "Firefox", "mozilla-vpn": "Mozilla VPN", "proton-vpn": "ProtonVPN"}


@dataclass
class Chunk:
    chunk_id: str      # "04-003" = article 4, third chunk
    article_id: int
    title: str
    url: str
    product: str
    section: str       # "Heading > Subheading"
    index: int         # position within the article
    body: str          # the article text only
    text: str          # prefix + body: this is what gets embedded and shown to the LLM


def wc(s: str) -> int:
    return len(s.split())


def split_sections(md: str, default_section: str = "Overview") -> list[tuple[str, str]]:
    """Return [(section_path, body)] using markdown headings as boundaries."""
    sections, stack, buf = [], [], []
    in_code = False

    def flush():
        body = "\n".join(buf).strip()
        if body:
            path = " > ".join(t for _, t in stack) or default_section
            sections.append((path, body))
        buf.clear()

    for line in md.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else HEADING_RE.match(line)
        if m:
            flush()
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, m.group(2)))
        else:
            buf.append(line)
    flush()
    return sections


def split_units(body: str) -> list[str]:
    """Break a section into paragraphs and individual list items."""
    units = []
    for para in re.split(r"\n\s*\n", body):
        cur = None
        for line in para.splitlines():
            if LIST_ITEM_RE.match(line):          # a top-level item starts a new unit
                if cur is not None:
                    units.append(cur)
                cur = line
            else:                                 # continuation / nested line
                cur = line if cur is None else cur + "\n" + line
        if cur is not None:
            units.append(cur)
    return [u.strip() for u in units if u.strip()]


def split_long(unit: str, max_words: int) -> list[str]:
    """Last resort: a single unit larger than max_words is cut by words."""
    words = unit.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


def pack(units: list[str], max_words: int, overlap_words: int) -> list[list[str]]:
    """Greedily pack units into chunks; carry trailing units forward as overlap."""
    flat = []
    for u in units:
        flat.extend(split_long(u, max_words) if wc(u) > max_words else [u])
    chunks, cur, cur_w, fresh = [], [], 0, 0
    for u in flat:
        w = wc(u)
        if cur and cur_w + w > max_words:
            chunks.append(cur)
            carry, cw = [], 0
            for p in reversed(cur):               # take trailing units up to overlap_words
                if cw + wc(p) > overlap_words:
                    break
                carry.insert(0, p)
                cw += wc(p)
            if cw + w > max_words:                # carry would overflow: drop it
                carry, cw = [], 0
            cur, cur_w, fresh = carry, cw, 0
        cur.append(u)
        cur_w += w
        fresh += 1
    if fresh:                                     # don't emit a chunk that is only overlap
        chunks.append(cur)
    return chunks


def make_prefix(title: str, product: str, section: str) -> str:
    return f"{title} [{PRODUCT_LABEL.get(product, product)}] > {section}"


def chunk_article(article: dict, md: str, max_words: int, overlap_words: int) -> list[Chunk]:
    out, idx = [], 0
    for section, body in split_sections(md):
        for units in pack(split_units(body), max_words, overlap_words):
            text_body = "\n".join(units)
            prefix = make_prefix(article["title"], article["product"], section)
            out.append(Chunk(
                chunk_id=f"{article['id']:02d}-{idx:03d}", article_id=article["id"],
                title=article["title"], url=article["url"], product=article["product"],
                section=section, index=idx, body=text_body, text=f"{prefix}\n{text_body}",
            ))
            idx += 1
    return out


def load_kb() -> list[tuple[dict, str]]:
    manifest = json.loads((config.KB_DIR / "manifest.json").read_text(encoding="utf-8"))
    return [(a, (config.KB_DIR / a["file"]).read_text(encoding="utf-8")) for a in manifest["articles"]]


def chunk_all(max_words: int | None = None, overlap_words: int | None = None) -> list[Chunk]:
    max_words = max_words or config.CHUNK_WORDS
    overlap_words = config.CHUNK_OVERLAP_WORDS if overlap_words is None else overlap_words
    chunks = []
    for article, md in load_kb():
        chunks.extend(chunk_article(article, md, max_words, overlap_words))
    return chunks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, help="print chunks of this article id")
    args = ap.parse_args()
    chunks = chunk_all()
    if args.show:
        for c in chunks:
            if c.article_id == args.show:
                print(f"--- {c.chunk_id} ({wc(c.body)} words) ---\n{c.text}\n")
    else:
        for aid in sorted({c.article_id for c in chunks}):
            cs = [c for c in chunks if c.article_id == aid]
            print(f"#{aid:02d} {cs[0].title[:50]:50} {len(cs):3} chunks, avg {sum(wc(c.body) for c in cs)//len(cs)} words")
        print(f"TOTAL {len(chunks)} chunks")