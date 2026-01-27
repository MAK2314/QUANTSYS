"""Simplified demo strategy using mock signals."""

from __future__ import annotations

from app.core.config import Settings
from app.core.decision import Decision, DecisionResult
from app.core.metrics import MetricSnapshot
from app.core.risk import can_risk
from app.engine.executor import ExecutionEngine


class DemoStrategy:
    """Evaluates trade conditions and triggers mock execution."""

    def __init__(self, executor: ExecutionEngine, settings: Settings) -> None:
        self.executor = executor
        self.settings = settings

    def run(
        self, price: float, probability: float, metrics: MetricSnapshot
    ) -> DecisionResult:
        """
        Evaluate trading rules and return a decision result.

        EV = (p * gain_pct - (1 - p) * loss_pct) * price
        """
        gain_pct = self.settings.expected_gain_pct
        loss_pct = self.settings.expected_loss_pct
        ev = (probability * gain_pct - (1 - probability) * loss_pct) * price

        if not self._guards(ev, metrics, price):
            return DecisionResult(
                decision=Decision.NO_TRADE,
                quantity=0.0,
                expected_value=ev,
            )

        return self.executor.build_decision(ev, price, probability)

    def _guards(self, ev: float, metrics: MetricSnapshot, price: float) -> bool:
        """Apply risk and performance gates."""
        if ev <= 0:
            return False
        if metrics.net_exposure >= self.settings.exposure_limit:
            return False
        if metrics.win_coverage_ratio < self.settings.min_wcr and metrics.win_coverage_ratio != 0:
            return False
        if not can_risk(
            wallet=self.executor.state.wallet_a,
            risk_fraction=self.settings.max_risk_per_trade,
            estimated_loss_pct=self.settings.expected_loss_pct,
        ):
            return False
        return price > 0

