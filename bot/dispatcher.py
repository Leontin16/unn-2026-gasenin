"""Dispatch updates to registered handlers."""

from typing import Any

from bot.handler import Handler, HandlerStatus


class Dispatcher:
    """Try handlers in order and stop when one handles an update."""

    def __init__(self, handlers: list[Handler]) -> None:
        self.handlers = handlers

    def dispatch(self, update: dict[str, Any]) -> None:
        for handler in self.handlers:
            if handler.can_handle(update) and handler.handle(update) is HandlerStatus.STOP:
                return
