import React, { useState } from 'react';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';
import ResultCard from './components/ResultCard';
import InfoPanel from './components/InfoPanel';
import { AlertCircle, RotateCcw } from 'lucide-react';

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
    <div className="flex flex-col min-h-screen bg-slate-50">
      <Header />

      {/* Hero strip */}
      <div className="px-6 py-6 text-black bg-gradient-to-r from-water-600 via-water-500 to-water-400">
        <div className="max-w-6xl mx-auto">
          <h2 className="mb-1 text-2xl font-bold font-display">
            Flood Risk Prediction System
          </h2>
          <p className="max-w-xl text-sm text-water-100">
            Enter location and weather data to run a two-stage machine learning prediction
            for flood occurrence, risk score, arrival time, and water height.
          </p>
        </div>
      </div>

      {/* Main layout */}
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 py-8 grid grid-cols-1 lg:grid-cols-[1fr_340px] gap-8 items-start">

        {/* ── Left: Form + Result ────────────────────────────────── */}
        <div className="space-y-6">

          {/* Form Card */}
          <div className="p-6 bg-white border rounded-2xl border-slate-100 shadow-card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-base font-bold text-slate-800">
                Input Parameters
              </h2>
              {(result || errMsg) && (
                <button
                  onClick={handleReset}
                  className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-600 transition-colors"
                >
                  <RotateCcw size={12} /> Reset
                </button>
              )}
            </div>
            <PredictionForm onResult={handleResult} onLoading={setLoading} />
          </div>

          {/* Error */}
          {errMsg && (
            <div className="flex items-start gap-3 p-5 border border-red-200 bg-red-50 rounded-2xl animate-fadeInUp">
              <AlertCircle size={20} className="text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-red-700">Prediction Error</p>
                <p className="text-xs text-red-500 mt-0.5">{errMsg}</p>
                <p className="mt-2 text-xs text-red-400">
                  Make sure the backend is running: <code className="px-1 font-mono bg-red-100 rounded">python main.py</code>
                </p>
              </div>
            </div>
          )}

          {/* Loading skeleton */}
          {loading && !result && (
            <div className="p-6 space-y-4 bg-white border rounded-2xl border-slate-100 shadow-card animate-pulse">
              <div className="h-16 bg-slate-100 rounded-xl" />
              <div className="grid grid-cols-2 gap-4">
                <div className="h-36 bg-slate-100 rounded-xl" />
                <div className="h-36 bg-slate-100 rounded-xl" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="h-16 bg-slate-100 rounded-xl" />
                <div className="h-16 bg-slate-100 rounded-xl" />
              </div>
            </div>
          )}

          {/* Result */}
          {result && !loading && (
            <div className="p-6 bg-white border rounded-2xl border-slate-100 shadow-card">
              <h2 className="mb-5 text-base font-bold text-slate-800">
                Prediction Result
              </h2>
              <ResultCard result={result} inputs={inputs} />
            </div>
          )}
        </div>

        {/* ── Right: Info Panel ──────────────────────────────────── */}
        <aside className="sticky hidden lg:block top-24">
          <InfoPanel />
        </aside>
      </div>

      {/* Footer */}
      <footer className="px-6 py-4 mt-4 bg-white border-t border-slate-100">
        <div className="flex items-center justify-between max-w-6xl mx-auto text-xs text-slate-400">
          <span>FloodSense · Colombo &amp; Gampaha Flood Risk Prediction</span>
        </div>
      </footer>
    </div>
  );
}
