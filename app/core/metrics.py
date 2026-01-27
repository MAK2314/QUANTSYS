"""Metric calculations for trading health and performance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from app.core.config import Settings
from app.models.position import Position
from app.models.trade import Trade
from app.models.wallet import Wallet


@dataclass
class MetricSnapshot:
    """Point-in-time metrics exposed via the API."""

    win_coverage_ratio: float
    daily_profit_sufficiency: float
    net_exposure: float
    drawdown_velocity: float


class MetricsEngine:
    """Calculates portfolio metrics with lightweight state for drawdown velocity."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._last_drawdown: float = 0.0

    def snapshot(
        self,
        wallet_a: Wallet,
        wallet_b: Wallet,
        positions: Iterable[Position],
        trades: Iterable[Trade],
        equity_peak: Optional[float],
    ) -> MetricSnapshot:
        """Compute all required metrics."""
        exposure = self._net_exposure(positions, wallet_a)
        wcr = self._win_coverage_ratio(trades)
        dps = self._daily_profit_sufficiency(wallet_a, wallet_b)
        ddv = self._drawdown_velocity(wallet_a, wallet_b, equity_peak)
        return MetricSnapshot(
            win_coverage_ratio=wcr,
            daily_profit_sufficiency=dps,
            net_exposure=exposure,
            drawdown_velocity=ddv,
        )

    def _win_coverage_ratio(self, trades: Iterable[Trade]) -> float:
        wins = sum(1 for t in trades if t.pnl > 0)
        losses = sum(1 for t in trades if t.pnl < 0)
        if losses == 0:
            return float(wins) if wins else 0.0
        return wins / losses

    def _daily_profit_sufficiency(self, wallet_a: Wallet, wallet_b: Wallet) -> float:
        """
        Measures realized profit against a lightweight daily target.

        Target is 0.5% of Wallet A's start-of-day balance.
        """
        target = wallet_a.start_of_day * 0.005
        if target == 0:
            return 0.0
        return wallet_b.balance / target

    def _net_exposure(
        self, positions: Iterable[Position], wallet_a: Wallet
    ) -> float:
        notional = sum(p.notional() for p in positions)
        if wallet_a.balance <= 0:
            return 0.0
        return min(notional / wallet_a.balance, 1.0)

    def _drawdown_velocity(
        self, wallet_a: Wallet, wallet_b: Wallet, equity_peak: Optional[float]
    ) -> float:
        """Rate of change of drawdown based on last observation."""
        equity = wallet_a.balance + wallet_b.balance
        if equity_peak is None:
            return 0.0
        drawdown = max(0.0, (equity_peak - equity) / equity_peak)
        velocity = drawdown - self._last_drawdown
        self._last_drawdown = drawdown
        return velocity

