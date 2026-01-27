"""Wallet models and helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Wallet:
    """Represents a segregated wallet."""

    name: str
    balance: float
    start_of_day: float

    def credit(self, amount: float) -> None:
        if amount <= 0:
            return
        self.balance += amount

    def debit(self, amount: float) -> None:
        if amount <= 0:
            return
        proposed = self.balance - amount
        if proposed < self.start_of_day:
            raise ValueError(f"{self.name} cannot drop below start-of-day balance")
        self.balance = proposed

    def reset_day(self, start_balance: float) -> None:
        self.start_of_day = start_balance
        self.balance = start_balance

