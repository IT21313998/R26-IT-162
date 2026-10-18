import React from 'react';
import {
  Brain, Database, ShieldCheck, Cpu, GitFork, Radio, CheckCircle, Award
} from 'lucide-react';

const FEATURES = [
  { name: 'District', desc: 'Colombo / Gampaha' },
  { name: 'Latitude & Longitude', desc: 'GPS WGS84 coordinates' },
  { name: 'Elevation (m)', desc: 'Topographic elevation (SRTM/DEM)' },
  { name: 'Distance to River (m)', desc: 'Euclidean distance to active channel' },
  { name: 'Land Cover', desc: 'Urban, Forest, Wetland, Agriculture' },
  { name: 'Soil Classification', desc: 'Clay, Sandy, Loamy, Peaty, Silty' },
  { name: 'Rainfall 7d (mm)', desc: '7-day antecedent precipitation' },
  { name: 'Monthly Rainfall (mm)', desc: '30-day baseline catchment volume' },
  { name: 'Rain Intensity (mm/hr)', desc: 'Peak storm burst precipitation' },
  { name: 'Historical Flood Count', desc: 'DMC 10-year empirical records' },
  { name: 'River Flow Rate (m³/s)', desc: 'Hydrometric gauge discharge rate' },
];

function InfoCard({ icon, title, subtitle, children }) {
  return (
    <div className="p-5 mb-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm">
      <div className="flex items-center gap-3 mb-3.5 pb-2.5 border-b border-slate-100">
        <div className="flex items-center justify-center w-8 h-8 rounded-xl bg-sky-50 text-water-600 border border-sky-100 shadow-xs">
          {React.cloneElement(icon, { size: 16, className: 'stroke-[2.2]' })}
        </div>
        <div>
          <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">{title}</h3>
          {subtitle && <p className="text-[10px] text-slate-400">{subtitle}</p>}
        </div>
      </div>
      {children}
    </div>
  );
}

export default function InfoPanel() {
  return (
    <div className="space-y-4">
      {/* CDAP Research Card */}
      <div className="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-sky-950 text-white shadow-md">
        <div className="flex items-center gap-2 mb-2">
          <Award size={16} className="text-water-400" />
          <span className="text-[11px] font-extrabold tracking-wider text-water-300 uppercase">
            SLIIT CDAP 2026
          </span>
        </div>
        <h4 className="text-sm font-bold leading-snug">
          Dual-Stage Flood Risk Scoring &amp; Inundation Forecasting (DFRS)
        </h4>
        <p className="text-[11px] text-slate-300 mt-1 leading-relaxed">
          Integrated with IoT real-time rainfall sensing array for localized early flood detection across Kelani &amp; Kalu river basins.
        </p>
      </div>

      {/* Model Architecture */}
      <InfoCard
        icon={<Brain />}
        title="Dual-Stage Pipeline"
        subtitle="Staged Machine Learning Architecture"
      >
        <div className="space-y-2.5">
          {[
            {
              stage: 'Stage 1A',
              name: 'XGBoost Classifier',
              desc: 'Flood Occurrence (Yes/No) + Confidence',
              tag: 'Classification',
            },
            {
              stage: 'Stage 1B',
              name: 'XGBoost Regressor',
              desc: 'Flood Risk Index (0 to 100 continuous score)',
              tag: 'Risk Scoring',
            },
            {
              stage: 'Stage 2',
              name: 'Multi-Output Regressor',
              desc: 'Arrival Window (hrs) & Peak Water Depth (m)',
              tag: 'Hydrology',
            },
          ].map(({ stage, name, desc, tag }) => (
            <div key={stage} className="p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex items-start gap-2.5">
              <span className="text-[9px] font-bold uppercase tracking-wider bg-water-100 text-water-800 px-1.5 py-0.5 rounded flex-shrink-0 mt-0.5">
                {stage}
              </span>
              <div className="min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-bold text-slate-800">{name}</p>
                </div>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </InfoCard>

      {/* Risk Thresholds */}
      <InfoCard
        icon={<ShieldCheck />}
        title="Risk Severity Matrix"
        subtitle="National Disaster Management Calibration"
      >
        <div className="space-y-2">
          {[
            { label: 'Very High', range: '≥ 70', color: '#dc2626', bg: 'bg-red-50 text-red-700 border-red-200' },
            { label: 'High', range: '50 – 69', color: '#ea580c', bg: 'bg-orange-50 text-orange-700 border-orange-200' },
            { label: 'Moderate', range: '30 – 49', color: '#d97706', bg: 'bg-amber-50 text-amber-700 border-amber-200' },
            { label: 'Low', range: '< 30', color: '#16a34a', bg: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
          ].map(({ label, range, color, bg }) => (
            <div
              key={label}
              className={`flex items-center justify-between px-3 py-1.5 rounded-xl border text-xs font-semibold ${bg}`}
            >
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
                <span>{label}</span>
              </div>
              <span className="font-mono text-[11px] opacity-80">Score {range}</span>
            </div>
          ))}
        </div>
      </InfoCard>

      {/* Feature Catalog */}
      <InfoCard
        icon={<Database />}
        title="Evaluated Features"
        subtitle="12 Multi-domain Input Vectors"
      >
        <div className="space-y-1.5 max-h-52 overflow-y-auto pr-1">
          {FEATURES.map(({ name, desc }) => (
            <div key={name} className="flex items-start justify-between gap-2 py-0.5 border-b border-slate-50 last:border-none">
              <span className="text-[11px] font-semibold text-slate-700">{name}</span>
              <span className="text-[10px] text-slate-400 text-right">{desc}</span>
            </div>
          ))}
        </div>
      </InfoCard>
    </div>
  );
}
