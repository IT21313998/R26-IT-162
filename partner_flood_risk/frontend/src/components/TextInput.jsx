import React from 'react';

export default function TextInput({ value, onChange, placeholder, type = 'text', step, min, max, unit, ...rest }) {
  return (
    <div className="relative flex items-center">
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        step={step}
        min={min}
        max={max}
        className={`w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-white
                   text-sm font-medium text-slate-800 placeholder-slate-300 shadow-sm
                   hover:border-slate-300 focus:border-water-500 focus:ring-4 focus:ring-water-500/10 focus:outline-none
                   transition-all duration-150 ${unit ? 'pr-12' : ''}`}
        {...rest}
      />
      {unit && (
        <span className="absolute right-3.5 text-xs font-semibold text-slate-400 pointer-events-none select-none">
          {unit}
        </span>
      )}
    </div>
  );
}
