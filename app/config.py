"""All settings come from .env (see .env.example)."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

KB_DIR = ROOT / "data" / "kb"
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_WORDS = int(os.getenv("CHUNK_WORDS", "150"))
CHUNK_OVERLAP_WORDS = int(os.getenv("CHUNK_OVERLAP_WORDS", "30"))
TOP_K = int(os.getenv("TOP_K", "3"))
CHROMA_DIR = ROOT / os.getenv("CHROMA_DIR", "data/chroma")
COLLECTION = os.getenv("COLLECTION", "mozilla_kb")
SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.30"))

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "120"))
NUM_CTX = int(os.getenv("NUM_CTX", "4096"))