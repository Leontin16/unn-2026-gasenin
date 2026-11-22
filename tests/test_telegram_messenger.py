"""Tests for Telegram Bot API request parameters."""

import json
import unittest
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlsplit

from bot.telegram_messenger import TelegramMessenger


class TelegramMessengerTests(unittest.TestCase):
    @patch("bot.telegram_messenger.urlopen")
    def test_get_updates_sends_required_long_poll_parameters(self, mock_urlopen: Mock) -> None:
        response = Mock()
        response.read.return_value = b'{"ok": true, "result": []}'
        mock_urlopen.return_value.__enter__.return_value = response
        messenger = TelegramMessenger("test-token", "https://api.example.test")

        self.assertEqual(messenger.get_updates(offset=0), [])

        request = mock_urlopen.call_args.args[0]
        query = parse_qs(urlsplit(request.full_url).query)
        self.assertEqual(query["offset"], ["0"])
        self.assertEqual(query["timeout"], ["30"])
        self.assertEqual(query["limit"], ["100"])
        self.assertEqual(json.loads(query["allowed_updates"][0]), ["message"])


if __name__ == "__main__":
    unittest.main()
