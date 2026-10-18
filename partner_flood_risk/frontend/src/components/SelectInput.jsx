import React from 'react';
import { ChevronDown } from 'lucide-react';

export default function SelectInput({ value, onChange, options, placeholder }) {
  return (
    <div className="relative">
      <select
        value={value}
        onChange={onChange}
        className="w-full px-3.5 py-2.5 pr-10 rounded-xl border border-slate-200 bg-white
                   text-sm font-medium text-slate-800 appearance-none cursor-pointer shadow-sm
                   hover:border-slate-300 focus:border-water-500 focus:ring-4 focus:ring-water-500/10 focus:outline-none
                   transition-all duration-150"
      >
        {placeholder && (
          <option value="" disabled>{placeholder}</option>
        )}
        {options.map((opt) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
      <ChevronDown size={16} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
    </div>
  );
}
