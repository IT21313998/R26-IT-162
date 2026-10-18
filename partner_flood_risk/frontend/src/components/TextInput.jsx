import React from 'react';

export default function TextInput({ value, onChange, placeholder, type = 'text', step, min, max, ...rest }) {
  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      step={step}
      min={min}
      max={max}
      className="w-full px-3 py-2.5 rounded-lg border border-slate-200 bg-white
                 text-sm text-slate-800 placeholder-slate-300
                 focus:border-water-500 focus:ring-2 focus:ring-water-100
                 transition-all duration-150"
      {...rest}
    />
  );
}
