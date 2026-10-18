import React from 'react';
import { Brain, Database, ShieldCheck, Cpu } from 'lucide-react';

const FEATURES = [
  { name: 'District',               desc: 'Colombo / Gampaha' },
  { name: 'Latitude & Longitude',   desc: 'GPS coordinates' },
  { name: 'Elevation (m)',          desc: 'From topographic map / GPS' },
  { name: 'Distance to River (m)',  desc: 'Google Maps / field' },
  { name: 'Land Cover',             desc: 'Urban, Forest, Wetland…' },
  { name: 'Soil Type',              desc: 'Clay, Sandy, Loamy…' },
  { name: 'Rainfall 7d (mm)',       desc: 'Weather app / station' },
  { name: 'Monthly Rainfall (mm)',  desc: 'Weather app / station' },
  { name: 'Rain Intensity (mm/hr)', desc: 'Peak rate' },
  { name: 'Historical Flood Count', desc: 'DMC / community records' },
  { name: 'River Flow Rate (m³/s)', desc: 'DMC / irrigation gauge' },
];

function InfoBlock({ icon, title, children }) {
  return (
    <div className="p-5 mb-4 bg-white border rounded-2xl border-slate-100 shadow-card">
      <div className="flex items-center gap-2.5 mb-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-water-50">
          {React.cloneElement(icon, { size: 16, className: 'text-water-600' })}
        </div>
        <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
      </div>
      {children}
    </div>
  );
}

export default function InfoPanel() {
  return (
    <div>
      <InfoBlock icon={<Brain />} title="Pipeline Architecture">
        <div className="space-y-2.5">
          {[
            { stage: 'Stage 1A', label: 'XGBoost Classifier', out: 'Flood Yes/No + Probability' },
            { stage: 'Stage 1B', label: 'XGBoost Regressor',  out: 'Risk Score (0–100)' },
            { stage: 'Stage 2',  label: 'Multi-Output XGBoost', out: 'Arrival Time + Water Height' },
          ].map(({ stage, label, out }) => (
            <div key={stage} className="flex items-start gap-3">
              <span className="text-[10px] font-mono font-bold text-water-600 bg-water-50 px-2 py-0.5 rounded mt-0.5 flex-shrink-0">
                {stage}
              </span>
              <div>
                <p className="text-xs font-semibold text-slate-700">{label}</p>
                <p className="text-[11px] text-slate-400">{out}</p>
              </div>
            </div>
          ))}
        </div>
      </InfoBlock>

      <InfoBlock icon={<ShieldCheck />} title="Risk Categories">
        {[
          { label: 'Very High', range: '≥ 70', color: '#dc2626' },
          { label: 'High',      range: '≥ 50', color: '#ea580c' },
          { label: 'Moderate',  range: '≥ 30', color: '#d97706' },
          { label: 'Low',       range: '< 30',  color: '#16a34a' },
        ].map(({ label, range, color }) => (
          <div key={label} className="flex items-center gap-2.5 mb-2">
            <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: color }} />
            <span className="w-20 text-xs font-semibold text-slate-700">{label}</span>
            <span className="text-xs text-slate-400">Score {range}</span>
          </div>
        ))}
      </InfoBlock>

      <InfoBlock icon={<Database />} title="Input Features (12)">
        <div className="space-y-1.5">
          {FEATURES.map(({ name, desc }) => (
            <div key={name} className="flex items-start justify-between gap-2">
              <span className="text-[11px] font-medium text-slate-600 leading-tight">{name}</span>
              <span className="text-[10px] text-slate-400 text-right leading-tight">{desc}</span>
            </div>
          ))}
        </div>
      </InfoBlock>

      
    </div>
  );
}
