import React from 'react';

export default function FormField({ label, hint, error, badge, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-center justify-between">
        <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider">
          {label}
        </label>
        {badge && (
          <span className="text-[10px] font-medium text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
            {badge}
          </span>
        )}
      </div>
      {children}
      {hint && !error && (
        <p className="text-[11px] text-slate-400 leading-tight">{hint}</p>
      )}
      {error && (
        <p className="text-[11px] text-rose-500 font-medium flex items-center gap-1">
          <span className="inline-block w-1 h-1 rounded-full bg-rose-500"></span>
          {error}
        </p>
      )}
    </div>
  );
}
