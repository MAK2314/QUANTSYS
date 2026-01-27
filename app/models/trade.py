"""Trade record used for metrics and persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.core.decision import Decision


@dataclass
class Trade:
    """Executed trade snapshot."""

    decision: Decision
    quantity: float
    price: float
    pnl: float
    timestamp: datetime
    signal_probability: Optional[float] = None

