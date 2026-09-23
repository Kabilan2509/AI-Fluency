"""Shared model configuration for the Day 2 assessment."""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

if PROVIDER == "ollama":
    BASE_URL, API_KEY = "http://localhost:11434/v1", "ollama"
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
elif PROVIDER == "groq":
    BASE_URL, API_KEY = "https://api.groq.com/openai/v1", os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
elif PROVIDER == "huggingface":
    BASE_URL, API_KEY = "https://router.huggingface.co/v1", os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
else:
    raise SystemExit("Unknown PROVIDER. Use ollama, groq, or huggingface.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Add it to .env.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


def banner(title: str) -> None:
    print(f"\n=== {title} | provider: {PROVIDER} | model: {MODEL} ===\n")
