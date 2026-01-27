export enum TradeType {
  EVENT = 'EVENT',
  MEAN_REVERSION = 'MEAN_REV',
  MOMENTUM = 'MOMENTUM',
  HEDGE = 'HEDGE'
}

export enum TradeStatus {
  OPEN = 'OPEN',
  CLOSED = 'CLOSED'
}

export interface Trade {
  id: string;
  time: string;
  asset: string;
  type: TradeType;
  size: number;
  price: number;
  pnl: number;
  status: TradeStatus;
}

export interface Wallet {
  currency: string;
  currentBalance: number;
  startBalance: number; // Added for day-start comparison
}

export interface RiskMetrics {
  wcr: number; // Win/Loss Consumption Ratio
  dps: number; // Daily Profit Score
  drawdownVelocity: number; // Speed of drawdown
  netExposurePercent: number; // Percentage
  deployedCapital: number; // Actual $ amount
}

export interface SystemStatus {
  timestamp: string;
  tradingAllowed: boolean;
  walletA: Wallet; // Trading Capital
  walletB: Wallet; // Profit Vault
  metrics: RiskMetrics;
  recentTrades: Trade[];
}
