import React, { useState, useEffect } from 'react';
import { Waves, Activity, ShieldCheck, ExternalLink, Cpu } from 'lucide-react';
import { healthCheck } from '../api';

export default function Header() {
  const [backendOnline, setBackendOnline] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const checkStatus = () => {
      healthCheck()
        .then(() => { if (isMounted) setBackendOnline(true); })
        .catch(() => { if (isMounted) setBackendOnline(false); });
    };
    checkStatus();
    const interval = setInterval(checkStatus, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-sm transition-all">
      <div className="flex items-center justify-between max-w-7xl px-4 sm:px-6 lg:px-8 py-3.5 mx-auto">
        {/* Brand & Project Metadata */}
        <div className="flex items-center gap-3.5">
          <div className="flex items-center justify-center w-11 h-11 rounded-2xl bg-gradient-to-tr from-sky-600 via-water-600 to-cyan-500 shadow-md shadow-water-500/20 text-white flex-shrink-0">
            <Waves size={22} className="stroke-[2.2]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-extrabold tracking-tight text-slate-900 font-display">
                FloodSense<span className="text-water-600">.AI</span>
              </h1>
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-200">
                SLIIT R26-IT-162
              </span>
            </div>
            <p className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
              <span>Dual-Stage Flood Forecasting</span>
              <span className="text-slate-300">•</span>
              <span className="text-water-700 font-medium">Kelani &amp; Kalu Basins</span>
            </p>
          </div>
        </div>

        {/* Right Status & Badges */}
        <div className="flex items-center gap-3">
          {/* Backend Status Pill */}
          <div className={`hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
            backendOnline === true
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
              : backendOnline === false
              ? 'bg-amber-50 text-amber-700 border-amber-200'
              : 'bg-slate-50 text-slate-500 border-slate-200'
          }`}>
            <span className="relative flex h-2 w-2">
              {backendOnline && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              )}
              <span className={`relative inline-flex rounded-full h-2 w-2 ${
                backendOnline === true
                  ? 'bg-emerald-500'
                  : backendOnline === false
                  ? 'bg-amber-500'
                  : 'bg-slate-400'
              }`}></span>
            </span>
            <span>
              {backendOnline === true
                ? 'ML Inference Engine Online'
                : backendOnline === false
                ? 'Backend Offline (Port 5000)'
                : 'Connecting ML Server...'}
            </span>
          </div>

          {/* Academic Badge */}
          <div className="hidden md:flex flex-col text-right pr-1 border-r border-slate-200">
            <span className="text-[11px] font-semibold text-slate-800">Faculty of Computing</span>
            <span className="text-[10px] text-slate-400">Research Viva Edition</span>
          </div>

          <a
            href="https://github.com/IT21313998/R26-IT-162"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200/80 hover:text-slate-900 border border-slate-200 transition-all duration-150"
            title="SLIIT CDAP Repository"
          >
            <span>Codebase</span>
            <ExternalLink size={12} className="text-slate-400" />
          </a>
        </div>
      </div>
    </header>
  );
}
