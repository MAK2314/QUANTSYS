import React from 'react';

interface ExposureBarProps {
  exposurePercent: number;
  deployedCapital: number;
}

const ExposureBar: React.FC<ExposureBarProps> = ({ exposurePercent, deployedCapital }) => {
  // Logic: Green <= 20, Yellow 20-35, Red > 35
  let status: 'safe' | 'warning' | 'danger' = 'safe';
  if (exposurePercent > 35) status = 'danger';
  else if (exposurePercent > 20) status = 'warning';

  const getColor = () => {
    if (status === 'safe') return 'bg-signal-success';
    if (status === 'warning') return 'bg-signal-warning';
    return 'bg-signal-danger';
  };

  const getTextColor = () => {
    if (status === 'safe') return 'text-signal-success';
    if (status === 'warning') return 'text-signal-warning';
    return 'text-signal-danger';
  };

  return (
    <div className="bg-white border border-gray-200 p-6 h-full flex flex-col justify-between">
      <div>
        <h3 className="text-gray-500 font-semibold text-xs uppercase tracking-widest mb-4">Capital in Market (Exposure)</h3>
        
        <div className="flex items-baseline gap-2 mb-1">
          <span className="text-2xl font-mono font-bold text-gray-900">
            ${deployedCapital.toLocaleString('en-US', { maximumFractionDigits: 0 })}
          </span>
          <span className={`font-mono text-sm font-bold ${getTextColor()}`}>
            ({exposurePercent.toFixed(1)}%)
          </span>
        </div>
      </div>

      <div className="w-full bg-gray-100 h-4 mt-4 relative overflow-hidden">
        {/* Threshold Markers */}
        <div className="absolute top-0 bottom-0 left-[20%] w-px bg-white z-10 border-l border-dashed border-gray-400 opacity-50"></div>
        <div className="absolute top-0 bottom-0 left-[35%] w-px bg-white z-10 border-l border-dashed border-gray-400 opacity-50"></div>
        
        <div 
          className={`h-full ${getColor()} transition-all duration-500 ease-out`}
          style={{ width: `${Math.min(exposurePercent, 100)}%` }}
        ></div>
      </div>
      
      <div className="flex justify-between mt-1 text-[10px] text-gray-400 font-mono uppercase">
        <span>0%</span>
        <span>20% (Safe)</span>
        <span>35% (Max)</span>
      </div>
    </div>
  );
};

export default ExposureBar;
