"""Long polling loop for Telegram updates."""

import time
from typing import Any

from bot.dispatcher import Dispatcher
from bot.messenger import Messenger


def poll_once(messenger: Messenger, dispatcher: Dispatcher, offset: int) -> int:
    """Fetch and dispatch one batch of updates; return the next offset."""
    updates = messenger.get_updates(
        offset=offset,
        timeout=30,
        limit=100,
        allowed_updates=("message",),
    )

    for update in updates:
        update_id = update.get("update_id")
        if isinstance(update_id, int):
            offset = max(offset, update_id + 1)
        dispatcher.dispatch(update)

    return offset


def start_long_polling(messenger: Messenger, dispatcher: Dispatcher) -> None:
    """Poll Telegram forever, retrying after temporary errors."""
    offset = 0
    while True:
        try:
            offset = poll_once(messenger, dispatcher, offset)
        except KeyboardInterrupt:
            raise
        except Exception:
            print("\nTelegram API error. Retrying in 2 seconds.")
            time.sleep(2)
