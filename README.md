# Support chatbot for Firefox and Mozilla VPN

This is a support chatbot for the take-home assignment. It answers questions using only 18 Mozilla Support articles. Every answer shows which article it came from. If the articles don't cover a question, the bot says so. It asks a short question when a message is unclear, and it passes the chat to a human when it can't help.

It runs fully on your own computer. It needs no paid service and no API key.

## What you need

- Python 3.10 or newer
- [Ollama](https://ollama.com), installed and running
- About 4 GB of free RAM
- An internet connection for the first setup (to download the models)

## Setup

Run these commands one at a time. They are for Windows. On Linux or macOS, use `source .venv/bin/activate` and `cp` instead of `.venv\Scripts\activate` and `copy`.

```
git clone https://github.com/sadhikaprasanna/chatbot.git
cd chatbot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Then get the language model and the settings file:

```
ollama pull llama3.2:3b
copy .env.example .env
```

Build the search index. This takes under a minute. The first run also downloads a small embedding model (about 90 MB).

```
python -m app.index
```

Start the app:

```
uvicorn app.main:app --port 8000
```

Open http://localhost:8000 in your browser and start chatting.

Notes:
- Run only one server process. Chat history is kept in memory.
- A normal answer takes about 25 to 50 seconds on a CPU. Replies that come from simple rules (clarify, refuse, handoff) take a fraction of a second.

## Models used (all free and local)

| Part | Choice |
|---|---|
| Language model | `llama3.2:3b` through Ollama |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (384 numbers per text) |
| Vector store | Chroma, with cosine similarity |

All settings are in `.env.example`. They include the model name, how many chunks to search, the refusal threshold and the chunk size.

## API

`POST /chat`

Request:

```json
{"session_id": "abc123", "message": "How do I clear my cache?"}
```

Response:

```json
{
  "status": "answered",
  "answer": "...",
  "citations": [{"title": "...", "url": "...", "section": "..."}],
  "handoff": null
}
```

`status` is one of `answered`, `clarify`, `out_of_scope` or `handoff`. The `handoff` field is only filled when the status is `handoff`. It then contains `summary`, `intent` and `articles_tried`.

`GET /health` returns `{"status": "ok"}`.

Quick test from a second terminal:

```
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"session_id\":\"t1\",\"message\":\"How do I clear my cache?\"}"
```

Each request is also written to `logs/requests.jsonl`. The log has the retrieved chunk ids, their scores, the time taken and the token counts.

## Tests and evaluation

```
pytest -q
python -m eval.retrieval_eval
python -m eval.run_eval --no-judge
python -m eval.experiments.chunk_sweep
```

- `pytest -q` runs the unit tests and the API format tests.
- `python -m eval.retrieval_eval` checks search only, without the language model. It shows hit rates and the score ranges used to pick the refusal threshold.
- `python -m eval.run_eval --no-judge` runs all 53 test cases in `eval/testset.json`. It takes about 25 minutes on a CPU.
- `python -m eval.experiments.chunk_sweep` compares chunk sizes.

The results and a table of failures are in `RESULTS.md`. The design choices are in `DESIGN.md`. The AI tools I used are listed in `AI_USAGE.md`.

## Knowledge base

The 18 articles were saved on 8 October 2026.

- The raw pages are in `data/raw/`.
- The cleaned text and details for each article (title, URL, headings, product, hash) are in `data/kb/`.
- To rebuild the cleaned text from the raw pages, run `python -m app.ingest --clean-only`.

No URL was dead, so none was skipped.

Why I saved the pages by hand: when a script requested a page, the site returned a 3,036-byte "Client Challenge" page instead of the article. This is a JavaScript bot check. Python `requests` could not get past it, and neither could a headless Chromium browser. So I opened each page in a normal browser and saved its HTML into `data/raw/`. The script in `app/ingest.py` then cleans those files. It keeps only the article body, removes the table of contents and the "Related articles" list, and marks steps for a specific system as `[Windows]`, `[macOS]` or `[Linux]`. It also skips any file that is the wrong article or a copy of another one.

Article 14's link in the assignment had extra redirect text in it. The bot cites the clean address of that page.

## Assumptions

- The bot hands off to a human on the second failed turn in a row. A failed turn is a clarify or a refusal. It also hands off at once if the user asks for a person.
- If someone asks for a VPN refund and does not name the VPN, the bot asks which one (Mozilla VPN or ProtonVPN). It only asks when both articles match.
- "Cancel my VPN" is answered from the ProtonVPN article, because only that article has cancel steps.
- The bot never says it cancelled or refunded anything. It explains the steps instead.
- A question about another browser or VPN (Chrome, Safari, NordVPN) or about Firefox for Android or iOS is refused. This rule applies when the question does not also mention Firefox.

## Known limitations

- A small model can still misread an article. In one test the bot said "Yes" to whether refreshing Firefox deletes saved passwords. The article says passwords are kept. My word-matching check cannot catch this kind of mistake.
- "Export bookmarks and import them into Chrome" is refused completely, because it names Chrome. It should answer the Firefox part.
- Some pages show different steps for different Firefox versions (for example "Help" and "Help and Report"). The cleaned text keeps both, so some steps read a little oddly. Some answers also mix Windows and macOS steps.
- When a user asks for a human in their first message, the handoff summary says the issue is "unclear", because there is nothing else to summarise yet.
- The 0.15 boost for chunks with numbered steps and the 0.05 article margin were set by hand and only checked on my 53 test cases.
- Answers are slow on a CPU. A GPU or a hosted model would fix this.

More detail on failures is in `RESULTS.md`.

## Credit

The article text comes from [Mozilla Support](https://support.mozilla.org). It is published under the Creative Commons Attribution-ShareAlike license (https://creativecommons.org/licenses/by-sa/3.0/). Portions are copyright individual mozilla.org contributors. The cleaned articles in `data/` stay under the same license.