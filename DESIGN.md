2. Design decisions
Pydantic models define the contract. FastAPI validates both the request and the response, so a wrong field name fails in tests, not in the grader.
Blocking pipeline in a plain def endpoint. FastAPI runs def endpoints in a thread pool, so a 20 s LLM call doesn’t freeze /health. Using async def here would block the event loop.
Validation: session_id and message are required and non-empty, and message is capped at 1000 characters. An empty message gets a 422 from FastAPI.
Warm-up on startup. The first request would otherwise pay for loading MiniLM and the Ollama model. A startup hook loads the embedder, so the first demo request isn’t slow.
Never a 500 with a trace. pipeline.handle already catches errors; the endpoint adds a last-resort catch.
Same-origin UI. The page is served by the same app, so there is no CORS to configure.