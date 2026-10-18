import React from 'react';

const RADIUS = 54;
const CIRCUMFERENCE = Math.PI * RADIUS; // semi-circle

function getRiskDetails(score) {
  if (score >= 70) {
    return {
      color: '#ef4444',
      gradientId: 'gauge-very-high',
      bgLight: '#fef2f2',
      textColor: 'text-red-700',
      badgeClass: 'bg-red-500 text-white shadow-sm shadow-red-500/30'
    };
  }
  if (score >= 50) {
    return {
      color: '#f97316',
      gradientId: 'gauge-high',
      bgLight: '#fff7ed',
      textColor: 'text-orange-700',
      badgeClass: 'bg-orange-500 text-white shadow-sm shadow-orange-500/30'
    };
  }
  if (score >= 30) {
    return {
      color: '#eab308',
      gradientId: 'gauge-mod',
      bgLight: '#fefce8',
      textColor: 'text-amber-700',
      badgeClass: 'bg-amber-500 text-white shadow-sm shadow-amber-500/30'
    };
  }
  return {
    color: '#10b981',
    gradientId: 'gauge-low',
    bgLight: '#ecfdf5',
    textColor: 'text-emerald-700',
    badgeClass: 'bg-emerald-500 text-white shadow-sm shadow-emerald-500/30'
  };
}

export default function RiskGauge({ score, category }) {
  const safeScore = typeof score === 'number' && !isNaN(score) ? score : 0;
  const pct = Math.min(Math.max(safeScore, 0), 100) / 100;
  const offset = CIRCUMFERENCE * (1 - pct);
  const details = getRiskDetails(safeScore);

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative">
        <svg width="150" height="85" viewBox="0 0 140 80" className="overflow-visible">
          <defs>
            <linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="35%" stopColor="#eab308" />
              <stop offset="70%" stopColor="#f97316" />
              <stop offset="100%" stopColor="#ef4444" />
            </linearGradient>
          </defs>

          {/* Background Track */}
          <path
            d="M 14 70 A 56 56 0 0 1 126 70"
            fill="none"
            stroke="#f1f5f9"
            strokeWidth="11"
            strokeLinecap="round"
          />

          {/* Active Arc */}
          <path
            d="M 14 70 A 56 56 0 0 1 126 70"
            fill="none"
            stroke={details.color}
            strokeWidth="11"
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={offset}
            style={{
              transition: 'stroke-dashoffset 1.2s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.6s ease',
            }}
          />

          {/* Numeric Value */}
          <text
            x="70"
            y="58"
            textAnchor="middle"
            fontSize="24"
            fontWeight="800"
            fill={details.color}
            fontFamily="'Plus Jakarta Sans', sans-serif"
          >
            {safeScore.toFixed(1)}
          </text>
          <text
            x="70"
            y="74"
            textAnchor="middle"
            fontSize="10"
            fontWeight="600"
            fill="#94a3b8"
            fontFamily="'Plus Jakarta Sans', sans-serif"
          >
            SCORE / 100
          </text>
        </svg>

        {/* Min / Max Labels */}
        <div className="flex justify-between w-full px-2 text-[10px] font-semibold text-slate-300 -mt-1">
          <span>0</span>
          <span>50</span>
          <span>100</span>
        </div>
      </div>

      <div className="mt-2.5">
        <span
          className={`px-3 py-1 rounded-full text-[11px] font-extrabold uppercase tracking-wider ${details.badgeClass}`}
        >
          {category || 'Unknown'} Risk
        </span>
      </div>
    </div>
  );
}
