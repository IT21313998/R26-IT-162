import React from 'react';
import { ChevronDown } from 'lucide-react';

export default function SelectInput({ value, onChange, options, placeholder }) {
  return (
    <div className="relative">
      <select
        value={value}
        onChange={onChange}
        className="w-full px-3 py-2.5 pr-9 rounded-lg border border-slate-200 bg-white
                   text-sm text-slate-800 appearance-none cursor-pointer
                   focus:border-water-500 focus:ring-2 focus:ring-water-100
                   transition-all duration-150"
      >
        {placeholder && (
          <option value="" disabled>{placeholder}</option>
        )}
        {options.map((opt) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
      <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
    </div>
  );
}
