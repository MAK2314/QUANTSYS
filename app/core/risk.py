"""Risk and exposure helpers."""

from __future__ import annotations

from typing import Iterable

from app.models.position import Position
from app.models.trade import Trade
from app.models.wallet import Wallet


def calculate_net_exposure(positions: Iterable[Position], wallet: Wallet) -> float:
    """
    Net exposure as notional divided by wallet equity.

    The positions list can be empty for flat books. Exposure is clipped at 1.0.
    """
    notional = sum(p.notional() for p in positions)
    if wallet.balance <= 0:
        return 0.0
    return min(notional / wallet.balance, 1.0)


def win_coverage_ratio(trades: Iterable[Trade]) -> float:
    """Return wins-to-losses ratio; returns 0 if no closed trades."""
    wins = sum(1 for t in trades if t.pnl > 0)
    losses = sum(1 for t in trades if t.pnl < 0)
    if losses == 0:
        return float(wins) if wins else 0.0
    return wins / losses


def can_risk(wallet: Wallet, risk_fraction: float, estimated_loss_pct: float) -> bool:
    """
    Determine if a trade is permitted under wallet floor constraints.

    The maximum tolerated loss is capped so Wallet A never drops below its floor.
    """
    risk_budget = wallet.start_of_day * risk_fraction
    floor_after_loss = wallet.balance - risk_budget
    projected_loss = wallet.balance * estimated_loss_pct
    return floor_after_loss >= wallet.start_of_day and projected_loss <= risk_budget

