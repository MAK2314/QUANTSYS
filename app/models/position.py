"""Simplified position model."""

from __future__ import annotations

from dataclasses import dataclass

from app.core.decision import Decision


@dataclass
class Position:
    """Directional position for exposure tracking."""

    decision: Decision
    quantity: float
    entry_price: float

    def notional(self) -> float:
        return abs(self.quantity * self.entry_price)

