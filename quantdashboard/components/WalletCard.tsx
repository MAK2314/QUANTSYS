import React from 'react';

interface WalletCardProps {
  title: string;
  mainValue: number;
  subValue: string; // The text below the main number
  status: 'safe' | 'warning' | 'danger';
  label: string; // The bottom label
}

const WalletCard: React.FC<WalletCardProps> = ({ 
  title, 
  mainValue, 
  subValue, 
  status,
  label
}) => {
  
  // Status Colors
  const getBorderColor = () => {
    switch(status) {
      case 'safe': return 'border-l-signal-success';
      case 'warning': return 'border-l-signal-warning';
      case 'danger': return 'border-l-signal-danger';
      default: return 'border-l-gray-300';
    }
  };

  const getTextColor = () => {
    switch(status) {
      case 'safe': return 'text-signal-success';
      case 'warning': return 'text-signal-warning';
      case 'danger': return 'text-signal-danger';
      default: return 'text-gray-900';
    }
  };

  return (
    <div className={`bg-white border border-gray-200 rounded-none shadow-sm p-6 border-l-4 ${getBorderColor()}`}>
      <div className="flex justify-between items-start mb-4">
        <h2 className="text-gray-500 font-semibold text-xs uppercase tracking-widest">{title}</h2>
        <div className={`h-2 w-2 rounded-full ${status === 'safe' ? 'bg-signal-success' : status === 'warning' ? 'bg-signal-warning' : 'bg-signal-danger'}`}></div>
      </div>
      
      <div className="mb-2">
        <span className={`text-4xl font-mono font-bold tracking-tight text-gray-900`}>
          ${mainValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </span>
      </div>

      <div className={`font-mono text-sm font-medium mb-4 ${getTextColor()}`}>
        {subValue}
      </div>

      <div className="pt-4 border-t border-gray-100">
        <p className="text-xs text-gray-400 font-medium uppercase tracking-wide">
          {label}
        </p>
      </div>
    </div>
  );
};

export default WalletCard;
