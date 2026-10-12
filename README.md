# chatbot

support.mozilla.org serves a JavaScript client challenge to scripted clients (plain requests got a 3,036-byte 'Client Challenge' page; headless Chromium was also blocked). Pages were saved from a normal browser on <date>

Known weaknesses to note in the README
The step boost of 0.15 is a hand-set weight. I’ll tune it against the full evaluation, not just this one question.
Chunk 01-001 shows “Help Help and Report” because the page has version-specific variants that my cleaner concatenates. It’s a small cleaning flaw, so list it as known.
The handoff summary says “User issue: unclear” when the user asks for a human on their first message. I’ll improve it once the pipeline is stable.

# Grounded Customer Support Agent (IVA) for Firefox & Mozilla VPN

A support chatbot that answers **only** from 18 Mozilla Support articles, cites the article it used, asks a clarifying question when a message is vague or ambiguous, refuses what the articles don't cover, and hands off to a human when it cannot help. Everything runs locally at zero cost (Ollama + local embeddings, no API keys).

## Setup (5 commands)

```bash
git clone https://github.com/sadhikaprasanna/chatbot.git && cd chatbot
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt   # Linux/macOS: source .venv/bin/activate
ollama pull llama3.2:3b && copy .env.example .env                                     # Linux/macOS: cp .env.example .env
python -m app.index                                                                   # builds the vector index (one command)
uvicorn app.main:app --port 8000                                                      # open http://localhost:8000
```

Requires Python 3.10+ and [Ollama](https://ollama.com) running. About 4 GB of free RAM is recommended. The first `app.index` run downloads the ~90 MB embedding model. Single worker only (sessions are in memory).

## Zero-cost run
- LLM: `llama3.2:3b` via local Ollama. Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (local, 384-d). Vector store: Chroma (local, cosine).
- No paid API and no API key anywhere. `.env.example` lists every setting (model, top-k, threshold, chunk size, context size).
- A CPU answer takes roughly 25-50 s. Refusals, clarifications and handoffs decided by rules return in milliseconds.

## API
- `POST /chat` with `{"session_id": "...", "message": "..."}` returns `{"status": "answered|clarify|out_of_scope|handoff", "answer": "...", "citations": [{"title","url","section"}], "handoff": {"summary","intent","articles_tried"} | null}`.
- `GET /health` returns `{"status": "ok"}`.
- Chat UI at `/`. Each request is logged to `logs/requests.jsonl` (retrieved chunk ids, scores, latency, token counts, decision reason).

## Tests and evaluation
```bash
pytest -q                          # unit + API schema tests (chunker, gate/refusal, sessions, history, API contract)
python -m eval.retrieval_eval      # retrieval-only: hit@k, score distributions, threshold sweep (no LLM)
python -m eval.run_eval --no-judge # full evaluation on eval/testset.json (53 cases, ~25 min on CPU)
python -m eval.experiments.chunk_sweep   # chunk size x overlap experiment
```
Results and the failure table are in `RESULTS.md`; design decisions and numbers are in `DESIGN.md`.

## Knowledge base snapshot
- 18 articles from support.mozilla.org, saved **2026-10-08**. Raw HTML is in `data/raw/`, cleaned Markdown plus metadata (title, URL, headings, product tag, SHA-256) in `data/kb/`. Rebuild the Markdown with `python -m app.ingest --clean-only`.
- **No URL was dead or skipped.** Article 14's PDF link carried a redirect query string; the canonical URL is cited.
- **Why the pages were saved manually:** the site answered scripted requests with a 3,036-byte "Client Challenge" page (JavaScript bot check). Plain `requests` got only that page, and headless Chromium was also blocked. I therefore saved each page's HTML from a normal browser into `data/raw/NN.html`, and `app/ingest.py` cleans it (selector `#doc-content`, drops the table of contents and "Related articles", labels OS-specific blocks as `[Windows]`, `[macOS]`, `[Linux]`). A safety check skips any file that is not the requested article or duplicates another.

## Assumptions
- **Handoff** happens on the **second consecutive** unsuccessful turn (clarify or out_of_scope), or immediately when the user asks for a person.
- **Refund questions** clarify ("Mozilla VPN or ProtonVPN?") only when no product is named and both VPN articles match. "Cancel my VPN" is answered from article 18, because only that article contains cancellation steps.
- **Action requests** ("cancel it now") are answered with the process from the articles; the bot never claims to have done anything.
- **Foreign products** (other browsers or VPNs, Firefox for Android/iOS) are refused by a rule when named without Firefox/ff. Known limitation: "export bookmarks and import them into Chrome" is refused entirely.
- Version-specific variants of a step that the site shows conditionally (for example "Help" vs "Help and Report") are both kept in the cleaned text, so some steps read slightly garbled.

## Known limitations
See `RESULTS.md` (failure table) and `DESIGN.md` §5. In short: a 3B model can still misread a source (for example answering "Yes" where the article says passwords are kept), and the lexical grounding check cannot catch that.

## Attribution
Knowledge-base text is from [Mozilla Support](https://support.mozilla.org), published under the Creative Commons Attribution-ShareAlike license (https://creativecommons.org/licenses/by-sa/3.0/). Content (c) individual mozilla.org contributors. The cleaned articles in `data/` remain under CC BY-SA.