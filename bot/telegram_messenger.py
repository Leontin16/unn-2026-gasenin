"""Telegram Bot API implementation of Messenger."""

import json
from typing import Any
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from bot.messenger import Messenger


class TelegramMessenger(Messenger):
    """Send requests to the configured Telegram Bot API."""

    def __init__(self, token: str, base_url: str) -> None:
        if not token:
            raise ValueError("Telegram token is empty")
        parsed_url = urlsplit(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("TELEGRAM_BASE_URL must be a valid HTTP(S) URL")
        self.api_url = f"{base_url.rstrip('/')}/bot{token}"

    def _request(
        self,
        method: str,
        params: dict[str, int] | None = None,
        body: dict[str, int | str] | None = None,
    ) -> Any:
        url = f"{self.api_url}/{method}"
        if params:
            url = f"{url}?{urlencode(params)}"

        data = None if body is None else json.dumps(body).encode("utf-8")
        headers = {} if data is None else {"Content-Type": "application/json"}
        request = Request(url, data=data, headers=headers)

        with urlopen(request, timeout=35) as response:
            result = json.loads(response.read().decode("utf-8"))

        if not result.get("ok"):
            raise RuntimeError("Telegram API returned an error")
        return result.get("result")

    def get_updates(self, offset: int, timeout: int = 30) -> list[dict[str, Any]]:
        result = self._request("getUpdates", params={"offset": offset, "timeout": timeout})
        return result if isinstance(result, list) else []

    def send_message(self, chat_id: int, text: str) -> None:
        self._request("sendMessage", body={"chat_id": chat_id, "text": text})
