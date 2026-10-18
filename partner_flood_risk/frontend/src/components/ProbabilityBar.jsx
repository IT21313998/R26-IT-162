import React from 'react';

export default function ProbabilityBar({ probability }) {
  const safeProb = typeof probability === 'number' && !isNaN(probability) ? probability : 0;
  const pct = (safeProb * 100).toFixed(1);

  const getStyle = (p) => {
    if (p >= 0.7) return { color: '#ef4444', bg: 'bg-red-500', text: 'High Certainty' };
    if (p >= 0.5) return { color: '#f97316', bg: 'bg-orange-500', text: 'Elevated' };
    if (p >= 0.3) return { color: '#eab308', bg: 'bg-amber-500', text: 'Moderate' };
    return { color: '#10b981', bg: 'bg-emerald-500', text: 'Minimal' };
  };

  const style = getStyle(safeProb);

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-1.5">
        <span className="text-xs text-slate-500 font-semibold tracking-wide">
          Flood Probability
        </span>
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
            {style.text}
          </span>
          <span className="text-sm font-extrabold font-mono" style={{ color: style.color }}>
            {pct}%
          </span>
        </div>
      </div>

      <div className="h-3 bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200/60">
        <div
          className={`h-full rounded-full transition-all duration-1000 ease-out ${style.bg}`}
          style={{ width: `${pct}%` }}
        />
      </div>

      <div className="flex justify-between mt-1.5 text-[10px] font-semibold text-slate-400">
        <span>0% (Safe)</span>
        <span className="text-slate-300">50% (Threshold)</span>
        <span>100% (Imminent)</span>
      </div>
    </div>
  );
}
