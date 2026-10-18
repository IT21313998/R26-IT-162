import React from 'react';
import {
  AlertTriangle, CheckCircle2, Clock, Droplets,
  TrendingUp, MapPin, BarChart3, ShieldAlert, Waves, Info
} from 'lucide-react';
import RiskGauge from './RiskGauge';
import ProbabilityBar from './ProbabilityBar';

function StatBox({ icon, label, value, unit, caption, color = '#0284c7', bgLight = '#f0f9ff' }) {
  return (
    <div className="p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-slate-500 font-semibold tracking-wide uppercase">
          {label}
        </span>
        <div
          className="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0"
          style={{ backgroundColor: bgLight }}
        >
          {React.cloneElement(icon, { size: 16, color })}
        </div>
      </div>
      <div>
        <p className="text-2xl font-extrabold text-slate-900 tracking-tight">
          {value}{' '}
          {unit && <span className="text-sm font-semibold text-slate-400">{unit}</span>}
        </p>
        {caption && (
          <p className="text-[11px] text-slate-400 mt-1 font-medium">{caption}</p>
        )}
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
    <div className="space-y-5 animate-fadeInUp">
      {/* ── Status Banner ────────────────────────────────────────── */}
      <div
        className={`rounded-2xl p-5 border shadow-sm transition-all ${
          isFlood
            ? 'bg-gradient-to-br from-red-500/10 via-rose-50 to-orange-50/50 border-red-300'
            : 'bg-gradient-to-br from-emerald-500/10 via-teal-50 to-cyan-50/50 border-emerald-300'
        }`}
      >
        <div className="flex items-start gap-4">
          <div className="mt-0.5 p-2 rounded-2xl flex-shrink-0 bg-white shadow-sm">
            {isFlood ? (
              <AlertTriangle size={30} className="text-red-600" />
            ) : (
              <CheckCircle2 size={30} className="text-emerald-600" />
            )}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span
                className={`text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full ${
                  isFlood
                    ? 'bg-red-600 text-white'
                    : 'bg-emerald-600 text-white'
                }`}
              >
                {isFlood ? 'Inundation Warning' : 'Basin Secure'}
              </span>
              <span className="text-xs font-semibold text-slate-500">
                {inputs?.district} District Target Locus
              </span>
            </div>
            <h3 className={`text-xl font-extrabold mt-1 tracking-tight ${
              isFlood ? 'text-red-950' : 'text-emerald-950'
            }`}>
              {isFlood
                ? 'Critical Flood Inundation Hazard Detected'
                : 'Hydrological Profile Within Normal Limits'}
            </h3>
            <p className={`text-xs mt-1 leading-relaxed ${
              isFlood ? 'text-red-700' : 'text-emerald-700'
            }`}>
              {isFlood
                ? `Projected flood onset in ~${arrivalH} hrs ${arrivalM} mins with estimated inundation height of ${result.water_height_m ? result.water_height_m.toFixed(2) : '1.5'} m.`
                : 'All soil saturation, upstream discharge, and antecedent precipitation indices remain under warning thresholds.'}
            </p>
          </div>
        </div>
      </div>

      {/* ── Stage 1: Gauge & Classification ──────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Risk Gauge Card */}
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-5 flex flex-col items-center justify-between">
          <div className="w-full flex items-center justify-between pb-2 border-b border-slate-100">
            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <BarChart3 size={14} className="text-water-600" />
              Stage 1B: Risk Score
            </p>
            <span className="text-[10px] font-semibold text-slate-400 bg-slate-100 px-2 py-0.5 rounded-md">
              0 - 100 Scale
            </span>
          </div>
          <div className="py-2">
            <RiskGauge score={result.flood_risk_score} category={result.risk_category} />
          </div>
          <p className="text-[11px] text-slate-400 text-center font-medium">
            Evaluated via XGBoost Hydrological Regressor
          </p>
        </div>

        {/* Stage 1A Probability Card */}
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp size={14} className="text-water-600" />
              Stage 1A: Classification
            </p>
            <span className="text-[10px] font-semibold text-slate-400 bg-slate-100 px-2 py-0.5 rounded-md">
              XGBoost Classifier
            </span>
          </div>

          <div className="py-3 space-y-4">
            <ProbabilityBar probability={result.flood_probability} />

            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span className="text-xs font-semibold text-slate-600">Model Decision</span>
              <span
                className={`font-extrabold px-3 py-1 rounded-lg text-xs uppercase tracking-wider text-white shadow-sm ${
                  isFlood ? 'bg-red-600' : 'bg-emerald-600'
                }`}
              >
                Flood Occurrence: {result.flood_occurrence}
              </span>
            </div>
          </div>

          <p className="text-[11px] text-slate-400 font-medium">
            Threshold calibrated at 50% Bayesian posterior
          </p>
        </div>
      </div>

      {/* ── Stage 2: Hydrometric Projections ─────────────────────── */}
      <div>
        <div className="flex items-center justify-between mb-3 px-1">
          <p className="text-xs text-slate-500 font-bold uppercase tracking-wider flex items-center gap-1.5">
            <Waves size={14} className="text-water-600" />
            Stage 2: Multi-Output Hydrometric Projections
          </p>
          <span className="text-[10px] font-mono text-slate-400">
            Regressors: Arrival + Depth
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <StatBox
            icon={<Clock />}
            label="Estimated Inundation Arrival Time"
            value={result.arrival_time_hrs != null ? `${arrivalH}h ${arrivalM}m` : 'N/A'}
            unit={result.arrival_time_hrs != null ? 'from storm onset' : ''}
            caption={isFlood ? 'Urgent evacuation/prep window' : 'No rapid wave front expected'}
            color={isFlood ? '#dc2626' : '#64748b'}
            bgLight={isFlood ? '#fef2f2' : '#f8fafc'}
          />
          <StatBox
            icon={<Droplets />}
            label="Peak Water Inundation Height"
            value={result.water_height_m != null ? result.water_height_m.toFixed(2) : '0.00'}
            unit="metres"
            caption={isFlood ? 'Projected water depth above baseline ground level' : 'Normal channel depth'}
            color={isFlood ? '#0284c7' : '#64748b'}
            bgLight={isFlood ? '#f0f9ff' : '#f8fafc'}
          />
        </div>
      </div>

      {/* ── Mitigation Guidelines ────────────────────────────────── */}
      {isFlood && (
        <div className="p-4 rounded-2xl bg-amber-50/80 border border-amber-200">
          <div className="flex items-center gap-2 mb-2 text-amber-900 font-bold text-xs uppercase tracking-wider">
            <ShieldAlert size={16} className="text-amber-600" />
            Recommended Civil Defense Action (DMC SOP)
          </div>
          <ul className="text-xs text-amber-800 space-y-1 list-disc list-inside">
            <li>Pre-position emergency flood relief boats and de-watering pumps in lower reaches.</li>
            <li>Alert Kelani Basin riparian communities within 200m of the active river channel.</li>
            <li>Disconnect ground-level electrical switchgear in basements and low-lying facilities.</li>
          </ul>
        </div>
      )}

      {/* ── Feature Input Audit ──────────────────────────────────── */}
      {inputs && (
        <details className="group bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
          <summary className="cursor-pointer text-xs font-bold text-slate-600 p-4 flex items-center justify-between hover:bg-slate-50 transition-colors select-none">
            <span className="flex items-center gap-2">
              <MapPin size={14} className="text-water-600" />
              Detailed Model Feature Parameters Audit (12 Inputs)
            </span>
            <span className="text-xs text-slate-400 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div className="p-4 pt-0 border-t border-slate-100 bg-slate-50/50">
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 pt-3">
              {Object.entries(inputs).map(([k, v]) => (
                <div key={k} className="p-2.5 rounded-xl bg-white border border-slate-200/60 shadow-xs">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    {k.replace(/_/g, ' ')}
                  </span>
                  <span className="text-xs font-bold font-mono text-slate-800 mt-0.5 block truncate">
                    {String(v)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </details>
      )}
    </div>
  );
}
