"""Ollama wrapper. Returns parsed JSON plus token counts."""
import json
import time

import requests

from app import config


class LLMError(Exception):
    pass


def chat_json(system: str, user: str, retries: int = 1) -> tuple[dict, dict]:
    """Call Ollama in JSON mode. Returns (parsed_json, usage)."""
    body = {
        "model": config.LLM_MODEL,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0, "num_ctx": config.NUM_CTX},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }
    last = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(f"{config.OLLAMA_HOST}/api/chat", json=body, timeout=config.LLM_TIMEOUT)
            if r.status_code != 200:
                raise requests.RequestException(f"HTTP {r.status_code}: {r.text[:300]}")
            data = r.json()
            usage = {"prompt_tokens": data.get("prompt_eval_count", 0),
                     "completion_tokens": data.get("eval_count", 0)}
            return json.loads(data["message"]["content"]), usage
        except (requests.RequestException, json.JSONDecodeError, KeyError) as exc:
            last = exc
            time.sleep(1)
    raise LLMError(f"{type(last).__name__}: {last}")