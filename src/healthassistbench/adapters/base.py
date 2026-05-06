from __future__ import annotations

from abc import ABC, abstractmethod

from healthassistbench.schemas import DialogueTurn


class AssistantAdapter(ABC):
    @abstractmethod
    def respond(self, history: list[DialogueTurn]) -> str:
        raise NotImplementedError
