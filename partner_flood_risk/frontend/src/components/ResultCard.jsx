import React from 'react';
import {
  AlertTriangle, CheckCircle2, Clock, Droplets,
  TrendingUp, MapPin, BarChart3
} from 'lucide-react';
import RiskGauge from './RiskGauge';
import ProbabilityBar from './ProbabilityBar';

function StatBox({ icon, label, value, unit, color = '#3b95f6' }) {
  return (
    <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-100 shadow-sm">
      <div className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
           style={{ backgroundColor: `${color}15` }}>
        {React.cloneElement(icon, { size: 20, color })}
      </div>
      <div className="min-w-0">
        <p className="text-xs text-slate-500 font-medium">{label}</p>
        <p className="text-base font-bold text-slate-800 truncate">
          {value} <span className="text-xs font-normal text-slate-400">{unit}</span>
        </p>
      </div>
    </div>
  );
}

export default function ResultCard({ result, inputs }) {
  const isFlood = result.flood_occurrence === 'Yes';

  const arrivalH = result.arrival_time_hrs != null ? Math.floor(result.arrival_time_hrs) : null;
  const arrivalM = result.arrival_time_hrs != null
    ? Math.round((result.arrival_time_hrs - Math.floor(result.arrival_time_hrs)) * 60)
    : null;

  const riskColor =
    result.risk_category === 'Very High' ? '#dc2626' :
    result.risk_category === 'High'      ? '#ea580c' :
    result.risk_category === 'Moderate'  ? '#d97706' : '#16a34a';

  return (
    <div className="animate-fadeInUp">
      {/* Status Banner */}
      <div
        className="rounded-2xl p-5 mb-5 flex items-start gap-4"
        style={{
          background: isFlood
            ? 'linear-gradient(135deg, #fef2f2, #fee2e2)'
            : 'linear-gradient(135deg, #f0fdf4, #dcfce7)',
          border: `1.5px solid ${isFlood ? '#fca5a5' : '#86efac'}`,
        }}
      >
        <div className="mt-0.5 flex-shrink-0">
          {isFlood
            ? <AlertTriangle size={28} className="text-red-500" />
            : <CheckCircle2 size={28} className="text-green-500" />}
        </div>
        <div>
          <p className="font-bold text-lg" style={{ color: isFlood ? '#b91c1c' : '#15803d' }}>
            {isFlood ? '⚠️ Flood Risk Detected' : '✅ No Flood Risk Detected'}
          </p>
          <p className="text-sm mt-0.5" style={{ color: isFlood ? '#ef4444' : '#16a34a' }}>
            {inputs.district} District
            {isFlood
              ? ` — Expect water in ${arrivalH}h ${arrivalM}m`
              : ' — Conditions appear safe'}
          </p>
        </div>
      </div>

      {/* Risk Gauge + Probability */}
      <div className="grid grid-cols-2 gap-4 mb-5">
        <div className="bg-white rounded-2xl border border-slate-100 shadow-card p-5 flex flex-col items-center gap-3">
          <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider flex items-center gap-1.5">
            <BarChart3 size={12} /> Risk Score
          </p>
          <RiskGauge score={result.flood_risk_score} category={result.risk_category} />
        </div>

        <div className="bg-white rounded-2xl border border-slate-100 shadow-card p-5 flex flex-col justify-center gap-4">
          <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider flex items-center gap-1.5">
            <TrendingUp size={12} /> Stage 1 Output
          </p>
          <ProbabilityBar probability={result.flood_probability} />
          <div className="flex items-center justify-between text-sm mt-1">
            <span className="text-slate-500">Occurrence</span>
            <span
              className="font-bold px-2 py-0.5 rounded-lg text-white text-xs"
              style={{ backgroundColor: riskColor }}
            >
              {result.flood_occurrence}
            </span>
          </div>
        </div>
      </div>

      {/* Stage 2 Details */}
      <div className="mb-4">
        <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mb-3 px-1">
          Stage 2 — Arrival & Height Prediction
        </p>
        <div className="grid grid-cols-2 gap-3">
          <StatBox
            icon={<Clock />}
            label="Arrival Time"
            value={result.arrival_time_hrs != null ? `${arrivalH}h ${arrivalM}m` : 'N/A'}
            unit={result.arrival_time_hrs != null ? 'from now' : ''}
            color={isFlood ? '#ea580c' : '#64748b'}
          />
          <StatBox
            icon={<Droplets />}
            label="Water Height"
            value={result.water_height_m != null ? result.water_height_m.toFixed(2) : 'N/A'}
            unit={result.water_height_m != null ? 'm' : ''}
            color={isFlood ? '#3b95f6' : '#64748b'}
          />
        </div>
      </div>

      {/* Input Summary */}
      <details className="group">
        <summary className="cursor-pointer text-xs text-slate-400 font-medium flex items-center gap-1.5 hover:text-slate-600 transition-colors px-1 select-none">
          <MapPin size={11} />
          View submitted inputs
          <span className="ml-auto text-[10px] group-open:rotate-180 transition-transform inline-block">▼</span>
        </summary>
        <div className="mt-3 bg-slate-50 rounded-xl p-4 border border-slate-100">
          <div className="grid grid-cols-2 gap-x-6 gap-y-1.5">
            {Object.entries(inputs).map(([k, v]) => (
              <div key={k} className="flex justify-between text-xs">
                <span className="text-slate-400 capitalize">{k.replace(/_/g, ' ')}</span>
                <span className="font-mono font-medium text-slate-700">{String(v)}</span>
              </div>
            ))}
          </div>
        </div>
      </details>
    </div>
  );
}
