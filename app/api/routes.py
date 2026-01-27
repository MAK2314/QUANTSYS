"""FastAPI routes for the trading demo API."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.config import Settings
from app.core.metrics import MetricsEngine, MetricSnapshot
from app.engine.demo_strategy import DemoStrategy
from app.engine.executor import ExecutionEngine, PortfolioState
from app.models.wallet import Wallet

router = APIRouter()

# Instantiate core components (stateless HTTP, stateful engine for the demo).
settings = Settings()
state = PortfolioState(
    wallet_a=Wallet(name="Wallet A", balance=settings.start_balance_a, start_of_day=settings.start_balance_a),
    wallet_b=Wallet(name="Wallet B", balance=settings.start_balance_b, start_of_day=settings.start_balance_b),
)
state.equity_peak = state.wallet_a.balance + state.wallet_b.balance
metrics_engine = MetricsEngine(settings)
executor = ExecutionEngine(state=state, settings=settings)
strategy = DemoStrategy(executor=executor, settings=settings)


class WalletView(BaseModel):
    currency: str
    currentBalance: float
    startBalance: float


class MetricsView(BaseModel):
    wcr: float
    dps: float
    drawdownVelocity: float
    netExposurePercent: float
    deployedCapital: float

class TradeView(BaseModel):
    id: str
    time: str
    asset: str
    type: str
    size: float
    price: float
    pnl: float
    status: str


class StatusResponse(BaseModel):
    timestamp: str
    tradingAllowed: bool
    walletA: WalletView
    walletB: WalletView
    metrics: MetricsView
    recentTrades: List[TradeView]


class TradeRequest(BaseModel):
    price: float = Field(..., gt=0)
    probability: float = Field(..., ge=0, le=1)


class TradeResponse(BaseModel):
    status: StatusResponse
    decision: str
    quantity: float
    price: float
    pnl: float
    message: str


@router.get("/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    """Return wallets and current metrics."""
    metrics = _snapshot()
    return StatusResponse(
        timestamp=datetime.utcnow().isoformat(),
        tradingAllowed=True,
        walletA=_to_wallet_view(state.wallet_a),
        walletB=_to_wallet_view(state.wallet_b),
        metrics=_to_metrics_view(metrics),
        recentTrades=_to_recent_trades(),
    )


@router.post("/trade", response_model=TradeResponse)
def run_trade(request: TradeRequest) -> TradeResponse:
    """Run demo strategy once."""
    metrics = _snapshot()
    decision_result = strategy.run(price=request.price, probability=request.probability, metrics=metrics)

    if decision_result.decision.value == "NO_TRADE" or decision_result.quantity <= 0:
        status = get_status()
        return TradeResponse(
            status=status,
            decision=decision_result.decision.value,
            quantity=0.0,
            price=request.price,
            pnl=0.0,
            message="Trade skipped due to guards or insufficient edge",
        )

    try:
        trade = executor.simulate(
            decision_result=decision_result, price=request.price, probability=request.probability
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    status = get_status()
    return TradeResponse(
        status=status,
        decision=trade.decision.value,
        quantity=trade.quantity,
        price=trade.price,
        pnl=trade.pnl,
        message="Trade executed",
    )


@router.post("/reset")
def reset_day() -> dict:
    """Reset day state for a clean slate."""
    state.reset(settings)
    return {"message": "Day state reset", "wallet_a": _to_wallet_view(state.wallet_a), "wallet_b": _to_wallet_view(state.wallet_b)}


def _snapshot() -> MetricSnapshot:
    return metrics_engine.snapshot(
        wallet_a=state.wallet_a,
        wallet_b=state.wallet_b,
        positions=state.positions,
        trades=state.trades,
        equity_peak=state.equity_peak,
    )


def _to_wallet_view(wallet: Wallet) -> WalletView:
    return WalletView(currency="USDT", currentBalance=wallet.balance, startBalance=wallet.start_of_day)


def _to_metrics_view(metrics: MetricSnapshot) -> MetricsView:
    exposure_percent = metrics.net_exposure * 100.0
    deployed_capital = state.wallet_a.balance * metrics.net_exposure
    return MetricsView(
        wcr=metrics.win_coverage_ratio,
        dps=min(100.0, metrics.daily_profit_sufficiency * 100.0),
        drawdownVelocity=metrics.drawdown_velocity,
        netExposurePercent=exposure_percent,
        deployedCapital=deployed_capital,
    )


def _to_recent_trades(limit: int = 25) -> List[TradeView]:
    """Map internal trades to the frontend trade table schema."""
    views: List[TradeView] = []
    for t in state.trades[-limit:][::-1]:
        views.append(
            TradeView(
                id=f"trd_{int(t.timestamp.timestamp() * 1000)}",
                time=t.timestamp.time().strftime("%H:%M:%S"),
                asset="MOCK-ASSET",
                type="MOMENTUM",
                size=float(t.quantity),
                price=float(t.price),
                pnl=float(t.pnl),
                status="CLOSED",
            )
        )
    return views

