"""Tests for the dispatcher."""

import unittest
from typing import Any
from unittest.mock import Mock

from bot.dispatcher import Dispatcher
from bot.handler import HandlerStatus


class DispatcherTests(unittest.TestCase):
    def test_dispatch_stops_after_handler_returns_stop(self) -> None:
        first = Mock()
        first.can_handle.return_value = True
        first.handle.return_value = HandlerStatus.STOP
        second = Mock()

        Dispatcher([first, second]).dispatch({"message": {"text": "Hi"}})

        first.handle.assert_called_once()
        second.can_handle.assert_not_called()

    def test_dispatch_continues_when_handler_returns_continue(self) -> None:
        first = Mock()
        first.can_handle.return_value = True
        first.handle.return_value = HandlerStatus.CONTINUE
        second = Mock()
        second.can_handle.return_value = True
        second.handle.return_value = HandlerStatus.STOP
        update: dict[str, Any] = {"message": {"text": "Hi"}}

        Dispatcher([first, second]).dispatch(update)

        first.handle.assert_called_once_with(update)
        second.handle.assert_called_once_with(update)
