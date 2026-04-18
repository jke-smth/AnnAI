import asyncio
import json
import os
from typing import Any, Dict, Optional
from urllib import error, request


class TextEngine:
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        logger: Any = None,
    ):
        self.model = model or os.getenv("ANNAI_OLLAMA_MODEL", "qwen3:4b")
        self.base_url = (base_url or os.getenv("ANNAI_OLLAMA_URL", "http://127.0.0.1:11434")).rstrip("/")
        self.logger = logger

    def _log(self, msg: str):
        if self.logger:
            self.logger.info(msg)

    async def generate(self, prompt: str, system: str = "", options: Optional[Dict[str, Any]] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system
        if options:
            payload["options"] = options

        self._log(f"[TextEngine] Requesting Ollama model '{self.model}'")
        response_json = await asyncio.to_thread(self._post_json, "/api/generate", payload)
        response_text = response_json.get("response", "")
        response_text_stripped = response_text.strip() if isinstance(response_text, str) else ""
        if not response_text_stripped:
            try:
                self._log(f"[TextEngine] Empty response JSON: {response_json}")
            except Exception:
                pass
            raise RuntimeError(f"Ollama returned an empty response: {response_json}")

        return response_text_stripped

    def _post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=120) as resp:
                body = resp.read().decode("utf-8")
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Ollama HTTP {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Could not reach Ollama at {self.base_url}: {exc.reason}") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON returned by Ollama: {body}") from exc
