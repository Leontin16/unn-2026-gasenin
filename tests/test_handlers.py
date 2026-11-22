"""Tests for message handlers."""

import unittest
from typing import Any
from unittest.mock import Mock, patch

from bot.handler import HandlerStatus
from bot.handlers.message_text import MessageTextHandler


class MessageTextHandlerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.messenger = Mock()
        self.handler = MessageTextHandler(self.messenger)

    @patch("builtins.print")
    def test_echoes_text_message(self, _print: Mock) -> None:
        update: dict[str, Any] = {"message": {"text": "Hello", "chat": {"id": 123}}}

        self.assertTrue(self.handler.can_handle(update))
        self.assertIs(self.handler.handle(update), HandlerStatus.STOP)
        self.messenger.send_message.assert_called_once_with(123, "Hello")

    def test_ignores_sticker_and_other_non_text_messages(self) -> None:
        updates = [
            {"message": {"sticker": {}, "chat": {"id": 123}}},
            {"message": {"document": {}, "chat": {"id": 123}}},
            {"message": {"voice": {}, "chat": {"id": 123}}},
            {"message": {"video_note": {}, "chat": {"id": 123}}},
        ]

        for update in updates:
            self.assertFalse(self.handler.can_handle(update))
            self.assertIs(self.handler.handle(update), HandlerStatus.CONTINUE)

        self.messenger.send_message.assert_not_called()
