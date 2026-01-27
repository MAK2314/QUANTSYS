"""Trade decision data structures."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    """Discrete trade actions."""

    BUY = "BUY"
    SELL = "SELL"
    NO_TRADE = "NO_TRADE"


@dataclass
class DecisionResult:
    """Outcome of strategy evaluation."""

    decision: Decision
    quantity: float = 0.0
    expected_value: float = 0.0

