import React from 'react';

const RADIUS = 54;
const CIRCUMFERENCE = Math.PI * RADIUS; // half circle

function getRiskColor(score) {
  if (score >= 70) return '#dc2626';
  if (score >= 50) return '#ea580c';
  if (score >= 30) return '#d97706';
  return '#16a34a';
}

export default function RiskGauge({ score, category }) {
  const pct = Math.min(Math.max(score, 0), 100) / 100;
  const offset = CIRCUMFERENCE * (1 - pct);
  const color = getRiskColor(score);

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="140" height="80" viewBox="0 0 140 80">
        {/* Track */}
        <path
          d="M 14 70 A 56 56 0 0 1 126 70"
          fill="none"
          stroke="#e2e8f0"
          strokeWidth="12"
          strokeLinecap="round"
        />
        {/* Progress */}
        <path
          d="M 14 70 A 56 56 0 0 1 126 70"
          fill="none"
          stroke={color}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 1s ease, stroke 0.5s ease' }}
        />
        {/* Score text */}
        <text x="70" y="62" textAnchor="middle" fontSize="22" fontWeight="700" fill={color} fontFamily="DM Sans">
          {score.toFixed(1)}
        </text>
        <text x="70" y="76" textAnchor="middle" fontSize="10" fill="#64748b" fontFamily="DM Sans">
          / 100
        </text>
      </svg>
      <span
        className="px-3 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider text-white"
        style={{ backgroundColor: color }}
      >
        {category}
      </span>
    </div>
  );
}
