import React, { useState } from 'react';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';
import ResultCard from './components/ResultCard';
import InfoPanel from './components/InfoPanel';
import { AlertCircle, RotateCcw, ShieldCheck, Activity, Layers, Sparkles } from 'lucide-react';

export default function App() {
  const [result, setResult]   = useState(null);
  const [inputs, setInputs]   = useState(null);
  const [errMsg, setErrMsg]   = useState(null);
  const [loading, setLoading] = useState(false);

  const handleResult = (data, payload, error) => {
    if (error) {
      setErrMsg(error);
      setResult(null);
    } else {
      setResult(data);
      setInputs(payload);
      setErrMsg(null);
    }
  };

  const handleReset = () => {
    setResult(null);
    setInputs(null);
    setErrMsg(null);
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-50 text-slate-800 font-sans">
      <Header />

      {/* ── Executive Hero Banner ───────────────────────────────── */}
      <section className="relative overflow-hidden bg-gradient-to-r from-slate-900 via-sky-950 to-slate-900 text-white border-b border-sky-900/50">
        {/* Ambient lighting effects */}
        <div className="absolute top-0 right-1/4 -mt-12 w-96 h-96 bg-water-500/15 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/3 -mb-12 w-72 h-72 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-sky-500/15 text-sky-300 border border-sky-400/30 mb-3 backdrop-blur-xs">
                <Sparkles size={13} className="text-sky-400" />
                <span>Undergraduate Research Project · R26-IT-162</span>
              </div>
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight font-display text-white">
                Dual-Stage Flood Risk &amp; Inundation Forecasting System
              </h2>
              <p className="mt-2 text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl font-normal">
                Multi-tier machine learning inference leveraging XGBoost classification, continuous risk regressive modeling, and multi-output hydrological forecasting for arrival window and water depth.
              </p>
            </div>

            {/* Quick Architecture KPI Pills */}
            <div className="flex flex-row md:flex-col gap-2.5 flex-wrap flex-shrink-0">
              <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white/5 border border-white/10 backdrop-blur-md">
                <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                <div>
                  <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Stage 1A Classifier</p>
                  <p className="text-xs font-bold text-white">F1 Score: 0.941</p>
                </div>
              </div>
              <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white/5 border border-white/10 backdrop-blur-md">
                <div className="w-2 h-2 rounded-full bg-sky-400"></div>
                <div>
                  <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Stage 1B Risk Regressor</p>
                  <p className="text-xs font-bold text-white">RMSE: 3.12 (Scale 0-100)</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Main Dashboard Workspace ────────────────────────────── */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-8 items-start">

        {/* ── Left Column: Form & Output ───────────────────────── */}
        <div className="space-y-6">

          {/* Form Header Card */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-card">
            <div className="flex items-center justify-between mb-5 pb-3 border-b border-slate-100">
              <div>
                <h2 className="text-base font-bold text-slate-900 tracking-tight">
                  Hydro-Topographic Parameter Configuration
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Input catchment parameters or select a viva demonstration preset
                </p>
              </div>
              {(result || errMsg) && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 transition-colors cursor-pointer"
                >
                  <RotateCcw size={12} /> Reset Form
                </button>
              )}
            </div>

            <PredictionForm onResult={handleResult} onLoading={setLoading} />
          </div>

          {/* Error Message */}
          {errMsg && (
            <div className="flex items-start gap-3.5 p-5 border border-rose-200 bg-rose-50/90 rounded-2xl animate-fadeInUp shadow-sm">
              <AlertCircle size={22} className="text-rose-500 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-bold text-rose-800">Inference Request Failed</p>
                <p className="text-xs text-rose-600 mt-1">{errMsg}</p>
                <div className="mt-3 p-2.5 rounded-xl bg-white/80 border border-rose-200/80 text-xs text-slate-600 font-mono">
                  Make sure backend is active: <code className="text-sky-700 font-bold">python app.py</code> in <code className="text-slate-800">flood-app\backend</code>
                </div>
              </div>
            </div>
          )}

          {/* Loading Skeleton */}
          {loading && !result && (
            <div className="p-6 space-y-4 bg-white border rounded-2xl border-slate-200/80 shadow-card animate-pulse">
              <div className="h-16 bg-slate-100 rounded-2xl" />
              <div className="grid grid-cols-2 gap-4">
                <div className="h-44 bg-slate-100 rounded-2xl" />
                <div className="h-44 bg-slate-100 rounded-2xl" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="h-20 bg-slate-100 rounded-2xl" />
                <div className="h-20 bg-slate-100 rounded-2xl" />
              </div>
            </div>
          )}

          {/* Result Card */}
          {result && !loading && (
            <div className="p-6 bg-white border rounded-2xl border-slate-200/80 shadow-card">
              <div className="flex items-center justify-between mb-5 pb-3 border-b border-slate-100">
                <div>
                  <h2 className="text-base font-bold text-slate-900 tracking-tight">
                    Dual-Stage Machine Learning Output
                  </h2>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Real-time classification, risk estimation, and multi-output hydrological projection
                  </p>
                </div>
                <span className="text-[11px] font-bold text-water-700 bg-water-50 border border-water-200 px-2.5 py-1 rounded-full">
                  Inference Complete
                </span>
              </div>

              <ResultCard result={result} inputs={inputs} />
            </div>
          )}
        </div>

        {/* ── Right Column: Info & Architecture Panel ──────────── */}
        <aside className="sticky top-20">
          <InfoPanel />
        </aside>
      </main>

      {/* ── Footer ──────────────────────────────────────────────── */}
      <footer className="px-6 py-6 mt-12 bg-white border-t border-slate-200/80 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-700">FloodSense.AI</span>
            <span>·</span>
            <span>SLIIT Faculty of Computing · CDAP 2026</span>
          </div>
          <div className="text-slate-400 text-center sm:text-right">
            Project R26-IT-162 · Dual-Stage Flood Risk Scoring &amp; Inundation Forecasting System
          </div>
        </div>
      </footer>
    </div>
  );
}
