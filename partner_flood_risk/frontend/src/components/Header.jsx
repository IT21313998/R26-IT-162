import React from 'react';
import { Waves, Github } from 'lucide-react';

export default function Header() {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-100">
      <div className="flex items-center justify-between max-w-6xl px-6 py-4 mx-auto">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center shadow-sm w-9 h-9 rounded-xl bg-gradient-to-br from-water-500 to-water-700">
            <Waves size={18} className="text-white" />
          </div>
          <div>
            <h1 className="text-base font-bold leading-none text-slate-800 font-display">
              FloodSense
            </h1>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Colombo & Gampaha Districts
            </p>
          </div>
        </div>

        
      </div>
    </header>
  );
}
