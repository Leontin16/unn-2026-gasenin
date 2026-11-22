"""Tests for Telegram Bot API request parameters."""

import json
import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlsplit

from bot.telegram_messenger import TelegramMessenger


class TelegramMessengerTests(unittest.TestCase):
    @patch("bot.telegram_messenger.urlopen")
    def test_get_updates_sends_required_long_poll_parameters_as_json(
        self, mock_urlopen: Mock
    ) -> None:
        response = Mock()
        response.read.return_value = b'{"ok": true, "result": []}'
        mock_urlopen.return_value.__enter__.return_value = response
        messenger = TelegramMessenger("test-token", "https://api.example.test")

        self.assertEqual(messenger.get_updates(offset=0), [])

        request = mock_urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(urlsplit(request.full_url).path, "/bottest-token/getUpdates")
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(body["offset"], 0)
        self.assertEqual(body["timeout"], 30)
        self.assertEqual(body["limit"], 50)
        self.assertEqual(body["allowed_updates"], ["message"])


if __name__ == "__main__":
    unittest.main()
