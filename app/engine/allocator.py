"""Position sizing utilities."""

from __future__ import annotations

from app.core.config import Settings
from app.models.wallet import Wallet


def allocate_quantity(
    price: float,
    expected_loss_pct: float,
    wallet: Wallet,
    settings: Settings,
) -> float:
    """
    Determine quantity based on risk budget and expected adverse move.

    Quantity is capped so the projected loss equals the max risk per trade.
    """
    if price <= 0:
        return 0.0
    risk_budget = wallet.balance * settings.max_risk_per_trade
    per_unit_loss = price * expected_loss_pct
    if per_unit_loss <= 0:
        return 0.0
    quantity = risk_budget / per_unit_loss
    return max(quantity, 0.0)

