import React from 'react';

interface MetricCardProps {
  label: string;
  value: string | number;
  status: 'safe' | 'warning' | 'danger';
  description?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ 
  label, 
  value, 
  status,
  description
}) => {
  
  const getTextColor = () => {
    switch(status) {
      case 'safe': return 'text-signal-success';
      case 'warning': return 'text-signal-warning';
      case 'danger': return 'text-signal-danger';
      default: return 'text-gray-900';
    }
  };

  return (
    <div className="bg-white border border-gray-200 p-5 flex flex-col justify-between hover:shadow-md transition-shadow">
      <div>
        <h3 className="text-gray-500 text-xs font-bold uppercase tracking-widest mb-2">{label}</h3>
        <span className={`text-2xl font-mono font-bold ${getTextColor()}`}>
          {value}
        </span>
      </div>
      {description && (
        <p className="text-xs text-gray-400 mt-2 font-medium">{description}</p>
      )}
    </div>
  );
};

export default MetricCard;
