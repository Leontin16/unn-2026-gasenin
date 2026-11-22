"""Messenger interface used by the application."""

from abc import ABC, abstractmethod
from typing import Any


class Messenger(ABC):
    """Interface for receiving updates and sending Telegram messages."""

    @abstractmethod
    def get_updates(
        self,
        offset: int,
        timeout: int = 30,
        limit: int = 50,
        allowed_updates: tuple[str, ...] = ("message",),
    ) -> list[dict[str, Any]]:
        """Return updates starting from offset."""

    @abstractmethod
    def send_message(self, chat_id: int, text: str) -> None:
        """Send a text message to a chat."""
