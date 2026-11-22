"""Registered message handlers."""

from bot.handler import Handler
from bot.handlers.message_text import MessageTextHandler
from bot.messenger import Messenger


def get_handlers(messenger: Messenger) -> list[Handler]:
    """Create the application's handlers."""
    return [MessageTextHandler(messenger)]
