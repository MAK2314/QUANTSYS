"""SQLAlchemy ORM schema for persistence."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Enum, Float, Integer

from app.core.decision import Decision
from app.db.database import Base


class TradeRecord(Base):
    """Minimal trade ledger."""

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    decision = Column(Enum(Decision), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    pnl = Column(Float, nullable=False)
    signal_probability = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class PositionRecord(Base):
    """Snapshot of last position for optional persistence."""

    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    decision = Column(Enum(Decision), nullable=False)
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

