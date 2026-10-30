"""Multi-provider LLM client over plain HTTPS (no SDK to install) with a deterministic fallback.

Supports:
- Google Gemini (API key, models like gemini-2.5-flash, gemini-1.5-flash)
- Anthropic Claude (API key, models like claude-sonnet-5-5, claude-3-haiku-20240307)
- OpenAI (API key, models like gpt-4o, gpt-4o-mini)

`complete()` returns None when there is no API key or the call fails; callers then use the
template text, so the demo never depends on the network. A `transport` can be injected for tests.
"""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
GEMINI_URL_TMPL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"


def _default_transport(url: str, headers: dict, body: dict, timeout: float) -> dict:
    req = urllib.request.Request(url, json.dumps(body).encode(), headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (fixed https URL)
        return json.loads(resp.read())


class LLM:
    def __init__(
        self,
        api_key: str | None,
        model: str = "auto",
        transport: Callable | None = None,
        timeout: float = 20.0,
        provider: str = "auto",
    ) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.transport = transport or _default_transport
        self.provider = self._resolve_provider(provider, api_key, model)
        self.model = self._resolve_model(self.provider, model)

    @staticmethod
    def _resolve_provider(provider: str, api_key: str | None, model: str) -> str:
        if provider and provider != "auto":
            return provider.lower()
        if not api_key:
            return "none"
        m = (model or "").lower()
        k = (api_key or "")
        if "gemini" in m or k.startswith("AIza"):
            return "gemini"
        if "claude" in m or k.startswith("sk-ant-"):
            return "anthropic"
        if "gpt" in m or k.startswith("sk-"):
            return "openai"
        if "gemini" in m:
            return "gemini"
        return "anthropic"

    @staticmethod
    def _resolve_model(provider: str, model: str) -> str:
        if model and model != "auto":
            return model
        if provider == "gemini":
            return "gemini-2.5-flash"
        if provider == "openai":
            return "gpt-4o-mini"
        return "claude-sonnet-5-5"

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def complete(self, system: str, user: str, max_tokens: int = 400) -> str | None:
        if not self.available:
            return None
        try:
            if self.provider == "gemini":
                url = GEMINI_URL_TMPL.format(model=self.model, key=self.api_key)
                headers = {"content-type": "application/json"}
                body = {
                    "contents": [{"role": "user", "parts": [{"text": user}]}],
                    "systemInstruction": {"parts": [{"text": system}]},
                    "generationConfig": {"maxOutputTokens": max_tokens},
                }
                data = self.transport(url, headers, body, self.timeout)
                candidates = data.get("candidates") or []
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text = "".join(p.get("text", "") for p in parts).strip()
                    return text or None
                return None

            if self.provider == "openai":
                headers = {
                    "authorization": f"Bearer {self.api_key}",
                    "content-type": "application/json",
                }
                body = {
                    "model": self.model,
                    "max_tokens": max_tokens,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                }
                data = self.transport(OPENAI_URL, headers, body, self.timeout)
                choices = data.get("choices") or []
                if choices:
                    text = choices[0].get("message", {}).get("content", "").strip()
                    return text or None
                return None

            # Anthropic Claude
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            body = {
                "model": self.model,
                "max_tokens": max_tokens,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            }
            data = self.transport(ANTHROPIC_URL, headers, body, self.timeout)
            text = "".join(
                b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"
            ).strip()
            return text or None
        except Exception:
            return None
