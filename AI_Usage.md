# AI usage

## Tools
- ChatGPT - For understanding and creating a roadmap with design specifications.
- **Claude (Anthropic chat assistant)** was my main tool throughout. 
- **Local models** (llama3.2:3b via Ollama; MiniLM embeddings) are part of the product, not development aids.

## What I used ChatGPT for
- **Planning:** turning the brief into an ordered implementation plan, choosing the stack, and a schedule.

## What I used Claude for
- **Scaffolding code:** first drafts of `ingest.py`, `chunker.py`, `index.py`, `retriever.py`, `safety.py`, `sessions.py`, `gate.py`, `llm.py`, `rewrite.py`, `generate.py`, `grounding.py`, `pipeline.py`, `main.py`, the chat page, the unit tests and the evaluation scripts.
- **Test-set drafting:** a first draft of the 53 labelled cases across the 14 categories, which I then reviewed.
- **Analysis:** discussing evaluation results, the failure table, and draft text for README, RESULTS and DESIGN.

## What I did myself
- Debugging - reading my tracebacks and logs with it (the bot-challenge page, Windows file-name and `#`-comment mistakes, missing config values, Ollama HTTP 500, wrong product tags, a pytest folder named `tests.py`).
- Ran every command and experiment on my own machine (chunk-size sweep, retrieval evaluation, threshold choice, full evaluations) and made the decisions from the numbers: 120/30 chunks, threshold 0.30, freezing the results at the final run.
- Diagnosed on my own data: that the site serves a JavaScript client challenge, that `View Source` had the real HTML, which saved pages were wrong, and which refusals were genuine hallucinations (t09, t29, t31).
- Manually saved the 18 pages, checked the cleaned articles against the live pages, and fixed the product tags.
- Reviewed answers against the articles for the manual faithfulness review.
- Rewrote DESIGN.md in my own words and checked every number in it against my results.

## Accountability
I read the code of every file in the repository. I can explain and change any part of it in the live session, including the chunker packing loop, the gate order, the support-ratio check and the sentence filter, session and handoff logic, and the eval metrics. Where Claude's suggestion was wrong, I found it in testing (for example the support check initially let through an answer with an invented `top` command and a wrong "Yes" for the passwords question), and I list those cases in RESULTS.md instead of hiding them.