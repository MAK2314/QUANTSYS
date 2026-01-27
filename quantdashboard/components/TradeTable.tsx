import React from 'react';
import { Trade, TradeStatus } from '../types';

interface TradeTableProps {
  trades: Trade[];
}

const TradeTable: React.FC<TradeTableProps> = ({ trades }) => {
  return (
    <div className="bg-white border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h3 className="text-gray-900 font-bold text-xs uppercase tracking-widest">Recent Activity Log</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-white border-b-2 border-gray-100 text-xs uppercase text-gray-400">
            <tr>
              <th className="px-6 py-4 font-bold tracking-wider">Asset</th>
              <th className="px-6 py-4 font-bold tracking-wider">Type</th>
              <th className="px-6 py-4 font-bold tracking-wider">Size</th>
              <th className="px-6 py-4 font-bold tracking-wider text-right">Price</th>
              <th className="px-6 py-4 font-bold tracking-wider text-right">PnL</th>
              <th className="px-6 py-4 font-bold tracking-wider text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 font-mono text-xs text-gray-600">
            {trades.map((trade) => {
              const isProfit = trade.pnl >= 0;
              return (
                <tr key={trade.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-3 font-bold text-gray-900">{trade.asset}</td>
                  <td className="px-6 py-3">
                    <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-[10px] uppercase font-bold tracking-wide">
                      {trade.type}
                    </span>
                  </td>
                  <td className="px-6 py-3">{trade.size.toFixed(3)}</td>
                  <td className="px-6 py-3 text-right">
                    {trade.price.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </td>
                  <td className={`px-6 py-3 text-right font-bold ${isProfit ? 'text-signal-success' : 'text-signal-danger'}`}>
                    {isProfit ? '+' : ''}{trade.pnl.toFixed(2)}
                  </td>
                  <td className="px-6 py-3 text-right">
                    <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase ${
                      trade.status === TradeStatus.OPEN ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 text-gray-500'
                    }`}>
                      {trade.status}
                    </span>
                  </td>
                </tr>
              );
            })}
            {trades.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-gray-400 italic">
                  No trades recorded today.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TradeTable;
