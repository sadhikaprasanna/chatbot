"""Two-stage ingestion of Mozilla Support articles.

Stage 1 (download): render each page in headless Chromium -> data/raw/NN.html
Stage 2 (clean):    raw HTML -> data/kb/NN-slug.md + data/kb/manifest.json

python -m app.ingest                  # both stages
python -m app.ingest --download-only  # just save raw HTML
python -m app.ingest --clean-only     # just clean (also for hand-saved HTML)
python -m app.ingest --headed         # show the browser window if headless is blocked
"""
import argparse
import datetime
import hashlib
import json
import time
import re
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as to_md

ROOT = Path(__file__).resolve().parent.parent
URLS_FILE = ROOT / "data" / "urls.json"
RAW_DIR = ROOT / "data" / "raw"
KB_DIR = ROOT / "data" / "kb"

# ASSUMPTIONS: confirm these with app/inspect_raw.py (step 1.5), then edit.
CONTENT_SELECTORS = ["#doc-content"]          # verified against the real page
JUNK_SELECTORS = ["script", "style", "form", "#toc", ".document-toc"]
OS_LABELS = {"win": "Windows", "mac": "macOS", "linux": "Linux",
             "android": "Android", "ios": "iOS"}


def slug_of(url: str) -> str:
    return url.split("?")[0].split("#")[0].rstrip("/").rsplit("/", 1)[-1]


# ---------- Stage 1: download ----------
def download_all(entries: list[dict], headed: bool) -> None:
    from playwright.sync_api import sync_playwright  # imported here so --clean-only needs no browser

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    sources = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(bypass_csp=True)  # page CSP can't block Playwright's own scripts
        page = context.new_page()
        for e in entries:
            rec = {"id": e["id"], "requested_url": e["url"], "final_url": None,
                   "status": None, "downloaded": today, "error": None}
            try:
                resp = page.goto(e["url"], wait_until="domcontentloaded", timeout=60000)
                rec["status"] = resp.status if resp else None
                if resp and resp.status in (404, 410):
                    rec["error"] = "dead page"
                else:
                    # Poll from Python (no in-page eval) until the challenge page is gone.
                    deadline = time.time() + 40
                    while page.title() == "Client Challenge" and time.time() < deadline:
                        page.wait_for_timeout(1000)
                    if page.title() == "Client Challenge":
                        raise RuntimeError("still on Client Challenge page after 40s")
                    page.wait_for_load_state("networkidle")
                    (RAW_DIR / f"{e['id']:02d}.html").write_text(page.content(), encoding="utf-8")
                    rec["final_url"] = page.url
            except Exception as exc:  # timeout, network error, still on challenge
                rec["error"] = f"{type(exc).__name__}: {str(exc)[:120]}"
            print(f"[{'OK' if not rec['error'] else 'FAIL'}] #{e['id']} {rec['error'] or rec['final_url']}")
            sources.append(rec)
        browser.close()
    (RAW_DIR / "sources.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")


# ---------- Stage 2: clean ----------
def process_data_for(node) -> None:
    """Handle SUMO's data-for blocks: drop non-Firefox boilerplate, label OS blocks,
    and add a space so adjacent variants don't glue together."""
    for block in node.select("[data-for]"):
        if block.decomposed:          # parent was already removed
            continue
        raw = block["data-for"].strip()
        if raw == "not fx":           # shown only to non-Firefox visitors
            block.decompose()
            continue
        tokens = [t.strip() for t in raw.split(",")]
        names = [OS_LABELS[t] for t in tokens if t in OS_LABELS]
        if names:
            block.insert(0, BeautifulSoup(f"<strong>[{' / '.join(names)}]</strong> ", "html.parser"))
        block.append(" ")


def extract(html: str) -> tuple[str, str, str, str | None]:
    """Return (title, markdown, selector_used, canonical_url)."""
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.select_one("h1.sumo-page-heading") or soup.find("h1")
    title = h1.get_text(strip=True) if h1 else (soup.title.get_text(strip=True) if soup.title else "")
    if title == "Client Challenge":
        raise ValueError("raw HTML is the bot-challenge page, not the article")
    canon = soup.find("link", rel="canonical")
    canonical = canon["href"] if canon and canon.get("href") else None
    node, used = None, None
    for sel in CONTENT_SELECTORS:
        node = soup.select_one(sel)
        if node:
            used = sel
            break
    if node is None:
        raise ValueError("no content container found; update CONTENT_SELECTORS")
    for junk in node.select(", ".join(JUNK_SELECTORS)):
        junk.decompose()
    process_data_for(node)
    md = to_md(str(node), heading_style="ATX", strip=["a", "img"])
    md = re.split(r"^#{1,6}\s+Related articles\s*$", md, flags=re.M | re.I)[0]  # cut link-only tail
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return title, md, used, canonical

def headings_of(md: str) -> list[str]:
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.*)$", md, re.M)]


def clean_all(entries: list[dict]) -> None:
    KB_DIR.mkdir(parents=True, exist_ok=True)
    sources_file = RAW_DIR / "sources.json"
    sources = {s["id"]: s for s in json.loads(sources_file.read_text())} if sources_file.exists() else {}
    articles, skipped = [], []
    for e in entries:
        raw = RAW_DIR / f"{e['id']:02d}.html"
        if not raw.exists():
            reason = sources.get(e["id"], {}).get("error") or "no raw HTML file"
            skipped.append({"id": e["id"], "url": e["url"], "reason": reason})
            print(f"[SKIP] #{e['id']} {reason}")
            continue
        try:
            title, md, used, canonical = extract(raw.read_text(encoding="utf-8"))
        except ValueError as exc:
            ...
        src = sources.get(e["id"], {})
        url = src.get("final_url") or canonical or e["url"]
        if canonical and canonical != e["url"]:
            print(f"      note: canonical URL differs from urls.json: {canonical}")
        src = sources.get(e["id"], {})
        url = src.get("final_url") or e["url"]
        date = src.get("downloaded") or datetime.date.fromtimestamp(raw.stat().st_mtime).isoformat()
        fname = f"{e['id']:02d}-{slug_of(url)}.md"
        (KB_DIR / fname).write_text(md, encoding="utf-8")
        words = len(md.split())
        flag = "  <-- SUSPICIOUSLY SHORT" if words < 150 else ""
        print(f"[OK] #{e['id']} {title!r}: {words} words via {used}{flag}")
        articles.append({
            "id": e["id"], "file": fname, "title": title, "url": url,
            "product": e["product"], "headings": headings_of(md), "word_count": words,
            "selector": used, "downloaded": date,
            "sha256": hashlib.sha256(md.encode("utf-8")).hexdigest(),
        })
    manifest = {"generated": datetime.date.today().isoformat(), "articles": articles, "skipped": skipped}
    (KB_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nSaved {len(articles)} articles, skipped {len(skipped)}.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--download-only", action="store_true")
    ap.add_argument("--clean-only", action="store_true")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()
    entries = json.loads(URLS_FILE.read_text())
    if not args.clean_only:
        download_all(entries, args.headed)
    if not args.download_only:
        clean_all(entries)


if __name__ == "__main__":
    main()