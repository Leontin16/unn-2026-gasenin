"""Application entry point."""

import os

from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers
from bot.long_polling import start_long_polling
from bot.telegram_messenger import TelegramMessenger


def main() -> None:
    token = os.environ.get("TELEGRAM_TOKEN")
    base_url = os.environ.get("TELEGRAM_BASE_URL")

    if not token or not base_url:
        raise SystemExit("Set TELEGRAM_TOKEN and TELEGRAM_BASE_URL environment variables")

    messenger = TelegramMessenger(token, base_url)
    dispatcher = Dispatcher(get_handlers(messenger))

    print("Bot is running. Press Ctrl+C to stop.")
    start_long_polling(messenger, dispatcher)


if __name__ == "__main__":
    main()
