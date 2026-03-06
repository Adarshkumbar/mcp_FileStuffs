from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import httpx


@dataclass(frozen=True)
class ChatResult:
    message: dict[str, Any]
    finish_reason: Optional[str]


class Ollama:
    """
    Minimal chat client for Ollama's OpenAI-compatible endpoint.

    Expects Ollama running at OLLAMA_BASE_URL (default http://localhost:11434).
    """

    def __init__(self, model: str, base_url: str):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=httpx.Timeout(120.0))

    def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 0.2,
    ) -> ChatResult:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        resp = self._client.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        data = resp.json()

        choice = (data.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        finish_reason = choice.get("finish_reason")
        return ChatResult(message=message, finish_reason=finish_reason)

