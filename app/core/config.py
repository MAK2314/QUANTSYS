"""Application configuration and constants."""

import os
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    app_name: str = Field("Quant Backend", description="Service name")
    database_url: str = Field(
        "sqlite:///./trading.db",
        env="DATABASE_URL",
        description="SQLAlchemy database URL (PostgreSQL recommended)",
    )
    max_risk_per_trade: float = Field(
        0.0025, description="Fraction of Wallet A allowed to risk per trade"
    )
    exposure_limit: float = Field(
        0.40, description="Maximum net exposure as fraction of Wallet A"
    )
    min_wcr: float = Field(1.1, description="Minimum win coverage ratio")
    expected_gain_pct: float = Field(
        0.01, description="Assumed favorable move used for EV sizing"
    )
    expected_loss_pct: float = Field(
        0.01, description="Assumed adverse move used for EV sizing"
    )
    expected_move_pct: float = Field(
        0.005, description="Typical move magnitude used in mock execution"
    )
    start_balance_a: float = Field(
        100_000.0, description="Start-of-day balance for trading wallet"
    )
    start_balance_b: float = Field(
        0.0, description="Start-of-day balance for profit vault"
    )
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="Allowed CORS origins for browser-based frontends (comma-separated)",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins from environment variable."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        if isinstance(v, list):
            return v
        # Check env var if not provided
        env_val = os.getenv("TRADING_CORS_ORIGINS")
        if env_val:
            return [origin.strip() for origin in env_val.split(",") if origin.strip()]
        return ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_prefix": "TRADING_"}

