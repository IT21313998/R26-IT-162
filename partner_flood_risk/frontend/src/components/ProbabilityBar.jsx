import React from 'react';

export default function ProbabilityBar({ probability }) {
  const pct = (probability * 100).toFixed(1);

  const color =
    probability >= 0.7 ? '#dc2626' :
    probability >= 0.5 ? '#ea580c' :
    probability >= 0.3 ? '#d97706' : '#16a34a';

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-1.5">
        <span className="text-xs text-slate-500 font-medium">Flood Probability</span>
        <span className="text-sm font-bold" style={{ color }}>{pct}%</span>
      </div>
      <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
      <div className="flex justify-between mt-1 text-[10px] text-slate-400">
        <span>0%</span>
        <span>50%</span>
        <span>100%</span>
      </div>
    </div>
  );
}
