import { SystemStatus, TradeType, TradeStatus, Trade } from '../types';

const RAW_API_URL = import.meta.env.VITE_API_BASE_URL;

if (!RAW_API_URL) {
  throw new Error("VITE_API_BASE_URL is not defined");
}

const API_BASE_URL = RAW_API_URL.replace(/\/+$/, "");

const generateMockData = (): SystemStatus => {
  const now = new Date();
  
  // Base capital logic
  const startCapA = 100000;
  const currentCapA = 100000 + (Math.random() * 2000 - 800); // Fluctuating around start
  
  const trades: Trade[] = Array.from({ length: 10 }).map((_, i) => ({
    id: `trd_${Date.now() - i * 10000}`,
    time: new Date(now.getTime() - i * 360000).toISOString().split('T')[1].slice(0, 8),
    asset: i % 3 === 0 ? 'BTC-PERP' : (i % 3 === 1 ? 'ETH-PERP' : 'SOL-PERP'),
    type: [TradeType.MOMENTUM, TradeType.MEAN_REVERSION, TradeType.HEDGE, TradeType.EVENT][Math.floor(Math.random() * 4)],
    size: Math.random() * 2 + 0.1,
    price: 64000 + Math.random() * 500,
    pnl: (Math.random() * 300) - 100,
    status: Math.random() > 0.3 ? TradeStatus.CLOSED : TradeStatus.OPEN
  }));

  const exposure = 15 + Math.random() * 25; // 15% to 40%

  return {
    timestamp: now.toISOString(),
    tradingAllowed: Math.random() > 0.05,
    walletA: {
      currency: 'USDT',
      startBalance: startCapA,
      currentBalance: currentCapA,
    },
    walletB: {
      currency: 'USDT',
      startBalance: 0,
      currentBalance: 850 + Math.random() * 200, // Profit vault
    },
    metrics: {
      wcr: 1.1 + Math.random() * 0.4,
      dps: 65 + Math.random() * 30,
      drawdownVelocity: 0.02 + Math.random() * 0.05,
      netExposurePercent: exposure,
      deployedCapital: currentCapA * (exposure / 100),
    },
    recentTrades: trades,
  };
};

export const fetchSystemStatus = async (): Promise<SystemStatus> => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1000);

    const response = await fetch(`${API_BASE_URL}/status`, {
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    return Promise.resolve(generateMockData());
  }
};
