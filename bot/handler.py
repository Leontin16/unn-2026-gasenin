"""Base class for update handlers."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class HandlerStatus(Enum):
    CONTINUE = "continue"
    STOP = "stop"


class Handler(ABC):
    """One link in the update handling chain."""

    @abstractmethod
    def can_handle(self, update: dict[str, Any]) -> bool:
        """Return whether this handler supports the update."""

    @abstractmethod
    def handle(self, update: dict[str, Any]) -> HandlerStatus:
        """Process the update and return the chain status."""
