from __future__ import annotations

import json
from typing import Any
from urllib import request

from healthassistbench.adapters.base import AssistantAdapter
from healthassistbench.schemas import DialogueTurn


class OllamaChatAdapter(AssistantAdapter):
    def __init__(
        self,
        model: str,
        host: str = "http://localhost:11434",
        system_prompt: str | None = None,
        timeout_seconds: int = 60,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.system_prompt = system_prompt
        self.timeout_seconds = timeout_seconds

    def respond(self, history: list[DialogueTurn]) -> str:
        messages: list[dict[str, Any]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        for turn in history:
            if turn.speaker == "patient":
                role = "user"
            elif turn.speaker == "assistant":
                role = "assistant"
            else:
                continue
            messages.append({"role": role, "content": turn.text})

        payload = json.dumps(
            {
                "model": self.model,
                "messages": messages,
                "stream": False,
            }
        ).encode("utf-8")
        http_request = request.Request(
            url=f"{self.host}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
        message = response_payload.get("message", {})
        return str(message.get("content", "")).strip()
