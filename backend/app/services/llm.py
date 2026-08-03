import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_ENV_PATH)

_client: OpenAI | None = None


def _normalize_base_url(url: str) -> str:
    url = url.rstrip("/")
    if not url.endswith("/v1"):
        url = f"{url}/v1"
    return url


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        base_url = os.getenv("OPENAI_BASE_URL")
        api_key = os.getenv("OPENAI_API_KEY")
        if not base_url or not api_key:
            raise RuntimeError("OPENAI_BASE_URL and OPENAI_API_KEY must be set in .env")
        _client = OpenAI(
            base_url=_normalize_base_url(base_url),
            api_key=api_key,
        )
    return _client


def get_model_name() -> str:
    return os.getenv("MODEL_NAME", "gpt-4.1-mini")


def chat(message: str) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=[{"role": "user", "content": message}],
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned an empty response")
    return content
