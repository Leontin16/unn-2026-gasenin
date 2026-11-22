"""Echo incoming text messages."""

from typing import Any

from bot.handler import Handler, HandlerStatus
from bot.messenger import Messenger


class MessageTextHandler(Handler):
    """Repeat text messages and ignore all other update types."""

    def __init__(self, messenger: Messenger) -> None:
        self.messenger = messenger

    def can_handle(self, update: dict[str, Any]) -> bool:
        message = update.get("message")
        return (
            isinstance(message, dict)
            and isinstance(message.get("text"), str)
            and isinstance(message.get("chat"), dict)
            and isinstance(message["chat"].get("id"), int)
        )

    def handle(self, update: dict[str, Any]) -> HandlerStatus:
        if not self.can_handle(update):
            return HandlerStatus.CONTINUE

        message = update["message"]
        self.messenger.send_message(message["chat"]["id"], message["text"])
        print(".", end="", flush=True)
        return HandlerStatus.STOP
