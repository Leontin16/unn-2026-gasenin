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
        self.requested_timeout = -1
        self.requested_limit = -1
        self.requested_allowed_updates: tuple[str, ...] = ()

    def get_updates(
        self,
        offset: int,
        timeout: int = 30,
        limit: int = 50,
        allowed_updates: tuple[str, ...] = ("message",),
    ) -> list[dict[str, Any]]:
        self.requested_offset = offset
        self.requested_timeout = timeout
        self.requested_limit = limit
        self.requested_allowed_updates = allowed_updates
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
        self.assertEqual(messenger.requested_timeout, 30)
        self.assertEqual(messenger.requested_limit, 50)
        self.assertEqual(messenger.requested_allowed_updates, ("message",))
        self.assertEqual(next_offset, 13)
        self.assertEqual(dispatcher.dispatch.call_count, 2)

    def test_poll_once_keeps_offset_when_no_updates(self) -> None:
        messenger = FakeMessenger([])
        dispatcher = Mock()

        self.assertEqual(poll_once(messenger, dispatcher, 7), 7)
        self.assertEqual(messenger.requested_offset, 7)
        self.assertEqual(messenger.requested_limit, 50)
        self.assertEqual(messenger.requested_allowed_updates, ("message",))
        dispatcher.dispatch.assert_not_called()
