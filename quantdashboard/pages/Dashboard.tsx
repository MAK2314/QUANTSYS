import React, { useEffect, useState } from 'react';
import { fetchSystemStatus } from '../services/api';
import { SystemStatus } from '../types';
import WalletCard from '../components/WalletCard';
import MetricCard from '../components/MetricCard';
import TradeTable from '../components/TradeTable';
import ExposureBar from '../components/ExposureBar';

const Dashboard: React.FC = () => {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const getData = async () => {
    try {
      const data = await fetchSystemStatus();
      setStatus(data);
      setLoading(false);
    } catch (error) {
      console.error("System disconnected");
    }
  };

  useEffect(() => {
    getData();
    const intervalId = setInterval(getData, 5000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading || !status) {
    return (
      <div className="flex h-screen items-center justify-center bg-white text-gray-900">
        <div className="flex flex-col items-center gap-4">
          <div className="h-2 w-24 bg-gray-100 overflow-hidden relative">
             <div className="absolute top-0 left-0 h-full w-12 bg-gray-900 animate-slide"></div>
          </div>
          <p className="text-xs font-mono uppercase tracking-widest text-gray-400">Connecting to Core...</p>
        </div>
        <style>{`
          @keyframes slide { 0% { left: -100%; } 100% { left: 100%; } }
          .animate-slide { animation: slide 1s infinite linear; }
        `}</style>
      </div>
    );
  }

  // --- Logic for Wallet A (Capital) ---
  const walletAChange = status.walletA.currentBalance - status.walletA.startBalance;
  const walletAPercent = (walletAChange / status.walletA.startBalance) * 100;
  const walletAStatus = walletAChange >= 0 ? 'safe' : 'danger';
  const walletASubValue = `${walletAChange >= 0 ? '+' : ''}${walletAPercent.toFixed(2)}% vs Start`;

  // --- Logic for Wallet B (Profit Vault) ---
  const profitRatio = (status.walletB.currentBalance / status.walletA.startBalance) * 100;
  let walletBStatus: 'safe' | 'warning' | 'danger' = 'danger';
  if (profitRatio >= 1.0) walletBStatus = 'safe';
  else if (profitRatio >= 0.3) walletBStatus = 'warning';
  
  const walletBSubValue = `${profitRatio.toFixed(2)}% of Capital`;

  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-12 font-sans selection:bg-gray-200">
      
      {/* Top Bar / Status Banner */}
      <header className="mb-8 flex justify-between items-center border-b-2 border-gray-900 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight uppercase">Quant<span className="text-gray-400">Sys</span></h1>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mt-1 font-mono">
            {new Date(status.timestamp).toLocaleTimeString()} — {status.tradingAllowed ? 'SYSTEM NOMINAL' : 'SYSTEM HALTED'}
          </p>
        </div>
        <div>
           <span className={`px-4 py-2 text-xs font-bold uppercase tracking-widest rounded-sm ${
             status.tradingAllowed ? 'bg-signal-success text-white' : 'bg-signal-danger text-white'
           }`}>
             {status.tradingAllowed ? 'Trading Allowed' : 'Trading Paused'}
           </span>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        
        {/* Wallet A */}
        <div className="lg:col-span-4">
          <WalletCard 
            title="Wallet A — Trading Capital"
            mainValue={status.walletA.currentBalance}
            subValue={walletASubValue}
            status={walletAStatus}
            label="Protected Capital — Must Never Go Below Start Value"
          />
        </div>

        {/* Wallet B */}
        <div className="lg:col-span-4">
          <WalletCard 
            title="Wallet B — Profit Vault"
            mainValue={status.walletB.currentBalance}
            subValue={walletBSubValue}
            status={walletBStatus}
            label="Realized Profit — Locked Until Day End"
          />
        </div>

        {/* Exposure */}
        <div className="lg:col-span-4">
          <ExposureBar 
             exposurePercent={status.metrics.netExposurePercent}
             deployedCapital={status.metrics.deployedCapital}
          />
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard 
          label="WCR Coverage"
          value={status.metrics.wcr.toFixed(2)}
          status={status.metrics.wcr > 1.2 ? 'safe' : (status.metrics.wcr > 1 ? 'warning' : 'danger')}
          description="Win/Loss Consumption Ratio"
        />
        <MetricCard 
          label="DPS Score"
          value={status.metrics.dps.toFixed(0)}
          status={status.metrics.dps > 70 ? 'safe' : (status.metrics.dps > 40 ? 'warning' : 'danger')}
          description="Daily Profit Sufficiency"
        />
        <MetricCard 
          label="Drawdown Velocity"
          value={status.metrics.drawdownVelocity.toFixed(4)}
          status={status.metrics.drawdownVelocity < 0.05 ? 'safe' : (status.metrics.drawdownVelocity < 0.1 ? 'warning' : 'danger')}
          description="Peak-to-trough decay rate"
        />
      </div>

      {/* Trade Feed */}
      <div className="w-full">
        <TradeTable trades={status.recentTrades} />
      </div>

    </div>
  );
};

export default Dashboard;
