"""Mock execution engine and portfolio state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple

from app.core.config import Settings
from app.core.decision import Decision, DecisionResult
from app.engine.allocator import allocate_quantity
from app.models.position import Position
from app.models.trade import Trade
from app.models.wallet import Wallet


@dataclass
class PortfolioState:
    """Holds intraday state for the demo engine."""

    wallet_a: Wallet
    wallet_b: Wallet
    positions: List[Position] = field(default_factory=list)
    trades: List[Trade] = field(default_factory=list)
    equity_peak: float | None = None

    def record_trade(self, trade: Trade) -> None:
        self.trades.append(trade)
        equity = self.wallet_a.balance + self.wallet_b.balance
        if self.equity_peak is None or equity > self.equity_peak:
            self.equity_peak = equity

    def reset(self, settings: Settings) -> None:
        self.wallet_a.reset_day(settings.start_balance_a)
        self.wallet_b.reset_day(settings.start_balance_b)
        self.positions.clear()
        self.trades.clear()
        self.equity_peak = self.wallet_a.balance + self.wallet_b.balance


class ExecutionEngine:
    """Executes mock trades and updates wallets and positions."""

    def __init__(self, state: PortfolioState, settings: Settings) -> None:
        self.state = state
        self.settings = settings

    def simulate(
        self, decision_result: DecisionResult, price: float, probability: float
    ) -> Trade:
        """Apply a mock execution and update wallets accordingly."""
        quantity = decision_result.quantity
        pnl = self._simulate_pnl(decision_result.decision, quantity, price, probability)
        if pnl >= 0:
            # Only realized profit can enter Wallet B.
            self.state.wallet_b.credit(pnl)
        else:
            self.state.wallet_a.debit(abs(pnl))

        trade = Trade(
            decision=decision_result.decision,
            quantity=quantity,
            price=price,
            pnl=pnl,
            timestamp=datetime.utcnow(),
            signal_probability=probability,
        )
        self._update_positions(trade)
        self.state.record_trade(trade)
        return trade

    def _simulate_pnl(
        self, decision: Decision, quantity: float, price: float, probability: float
    ) -> float:
        """
        Mock PnL based on probability-driven move.

        Movement factor ranges [-1, 1]; expected_move_pct controls magnitude.
        """
        if decision is Decision.NO_TRADE or quantity <= 0:
            return 0.0
        movement_factor = (probability - 0.5) * 2.0
        direction = 1.0 if decision is Decision.BUY else -1.0
        move_pct = self.settings.expected_move_pct * movement_factor * direction
        return price * quantity * move_pct

    def _update_positions(self, trade: Trade) -> None:
        """
        Simplified position tracking for exposure.

        Positions are overwritten per trade to avoid long-lived state for the demo.
        """
        if trade.quantity <= 0 or trade.decision is Decision.NO_TRADE:
            self.state.positions.clear()
            return
        self.state.positions = [
            Position(decision=trade.decision, quantity=trade.quantity, entry_price=trade.price)
        ]

    def build_decision(
        self, ev: float, price: float, probability: float
    ) -> DecisionResult:
        """
        Choose action and size based on EV and risk.

        Uses max risk per trade and expected loss pct for sizing.
        """
        if ev <= 0 or price <= 0:
            return DecisionResult(decision=Decision.NO_TRADE, quantity=0.0, expected_value=ev)

        decision = Decision.BUY if probability >= 0.5 else Decision.SELL
        quantity = allocate_quantity(
            price=price,
            expected_loss_pct=self.settings.expected_loss_pct,
            wallet=self.state.wallet_a,
            settings=self.settings,
        )
        if quantity <= 0:
            return DecisionResult(decision=Decision.NO_TRADE, quantity=0.0, expected_value=ev)
        return DecisionResult(decision=decision, quantity=quantity, expected_value=ev)

