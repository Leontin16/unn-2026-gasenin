"""Tests for long polling."""

import unittest
from typing import Any
from unittest.mock import Mock

from bot.long_polling import poll_once
from bot.messenger import Messenger


class FakeMessenger(Messenger):
    def __init__(self, updates: list[dict[str, Any]]) -> None:
        self.updates = updates
        self.requested_offset = -1

    def get_updates(self, offset: int, timeout: int = 30) -> list[dict[str, Any]]:
        self.requested_offset = offset
        _ = timeout
        return self.updates

    def send_message(self, chat_id: int, text: str) -> None:
        pass


class LongPollingTests(unittest.TestCase):
    def test_poll_once_dispatches_updates_and_advances_offset(self) -> None:
        updates = [{"update_id": 10}, {"update_id": 12}]
        messenger = FakeMessenger(updates)
        dispatcher = Mock()

        next_offset = poll_once(messenger, dispatcher, 5)

        self.assertEqual(messenger.requested_offset, 5)
        self.assertEqual(next_offset, 13)
        self.assertEqual(dispatcher.dispatch.call_count, 2)

    def test_poll_once_keeps_offset_when_no_updates(self) -> None:
        messenger = FakeMessenger([])
        dispatcher = Mock()

        self.assertEqual(poll_once(messenger, dispatcher, 7), 7)
        dispatcher.dispatch.assert_not_called()
