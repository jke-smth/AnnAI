import asyncio
import os
from urllib import error, request

import pytest
from unittest.mock import patch

from annai.services.text_engine import TextEngine


def test_generate_success():
    engine = TextEngine(model="qwen3:4b", base_url="http://127.0.0.1:11434")
    with patch.object(TextEngine, "_post_json", return_value={"response": "Hello from model"}):
        out = asyncio.run(engine.generate("Say hi"))
        assert isinstance(out, str) and out.strip() != ""
        # log the output for debugging
        print(f"Generated output: '{out}'")


def test_generate_empty_response_raises():
    engine = TextEngine(model="qwen3:4b")
    with patch.object(TextEngine, "_post_json", return_value={"response": ""}):
        with pytest.raises(RuntimeError, match="Ollama returned an empty response"):
            asyncio.run(engine.generate("prompt"))


def test_generate_integration_with_ollama():
    base_url = os.getenv("ANNAI_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.getenv("ANNAI_OLLAMA_MODEL", "qwen3:4b")

    if not _ollama_is_available(base_url):
        pytest.skip(f"Ollama is not reachable at {base_url}")

    engine = TextEngine(model=model, base_url=base_url)
    out = asyncio.run(
        engine.generate(
            "Reply with a very short greeting and include the word 'AnnAI'.",
            system="Keep the reply under 12 words.",
        )
    )

    assert isinstance(out, str) and out.strip() != ""
    print(f"Ollama integration output: '{out}'")


def _ollama_is_available(base_url: str) -> bool:
    req = request.Request(f"{base_url}/api/tags", method="GET")
    try:
        with request.urlopen(req, timeout=3):
            return True
    except (error.URLError, error.HTTPError, TimeoutError):
        return False
