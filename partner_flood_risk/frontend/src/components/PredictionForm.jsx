import React, { useState, useEffect } from 'react';
import {
  MapPin, Cloud, Layers, History, Loader2, Zap
} from 'lucide-react';
import FormField from './FormField';
import TextInput from './TextInput';
import SelectInput from './SelectInput';
import { predict as apiPredict, getOptions } from '../api';

const DEFAULTS = {
  district: 'Colombo',
  latitude: 6.9271,
  longitude: 79.8612,
  elevation_m: 5,
  distance_to_river_m: 150,
  landcover: 'Urban',
  soil_type: 'Clay',
  rainfall_7d_mm: 200,
  monthly_rainfall_mm: 350,
  rainfall_intensity_mmhr: 15,
  historical_flood_count: 2,
  river_flow_rate_m3s: 120,
};

function SectionHeader({ icon, title }) {
  return (
    <div className="flex items-center gap-2 pb-2 mb-4 border-b border-slate-100">
      <div className="flex items-center justify-center rounded-lg w-7 h-7 bg-water-50">
        {React.cloneElement(icon, { size: 14, className: 'text-water-600' })}
      </div>
      <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
    </div>
  );
}

export default function PredictionForm({ onResult, onLoading }) {
  const [form, setForm] = useState(DEFAULTS);
  const [options, setOptions] = useState({
    districts: ['Colombo', 'Gampaha'],
    landcovers: ['Urban', 'Agriculture', 'Wetland', 'Forest', 'Plantation', 'Scrub', 'Bare Soil'],
    soil_types: ['Clay', 'Peaty', 'Silty', 'Loamy', 'Sandy'],
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    getOptions()
      .then(r => setOptions(r.data))
      .catch(() => {}); // fallback to defaults above
  }, []);

  const set = (key) => (e) => {
    const val = e.target ? e.target.value : e;
    setForm(prev => ({ ...prev, [key]: val }));
    setErrors(prev => ({ ...prev, [key]: undefined }));
  };

  const validate = () => {
    const errs = {};
    const nums = [
      'latitude', 'longitude', 'elevation_m', 'distance_to_river_m',
      'rainfall_7d_mm', 'monthly_rainfall_mm', 'rainfall_intensity_mmhr',
      'historical_flood_count', 'river_flow_rate_m3s'
    ];
    nums.forEach(k => {
      if (form[k] === '' || isNaN(Number(form[k]))) {
        errs[k] = 'Enter a valid number';
      }
    });
    if (!form.district) errs.district = 'Required';
    if (!form.landcover) errs.landcover = 'Required';
    if (!form.soil_type) errs.soil_type = 'Required';
    return errs;
  };

  const handleSubmit = async () => {
    const errs = validate();
    if (Object.keys(errs).length > 0) { setErrors(errs); return; }

    setLoading(true);
    onLoading(true);
    try {
      const payload = {
        ...form,
        latitude: Number(form.latitude),
        longitude: Number(form.longitude),
        elevation_m: Number(form.elevation_m),
        distance_to_river_m: Number(form.distance_to_river_m),
        rainfall_7d_mm: Number(form.rainfall_7d_mm),
        monthly_rainfall_mm: Number(form.monthly_rainfall_mm),
        rainfall_intensity_mmhr: Number(form.rainfall_intensity_mmhr),
        historical_flood_count: Number(form.historical_flood_count),
        river_flow_rate_m3s: Number(form.river_flow_rate_m3s),
      };
      const res = await apiPredict(payload);
      onResult(res.data, payload);
    } catch (err) {
      onResult(null, null, err?.response?.data?.error || 'Prediction failed. Check backend.');
    } finally {
      setLoading(false);
      onLoading(false);
    }
  };

  const num = (key, label, hint, step = 'any') => (
    <FormField label={label} hint={hint} error={errors[key]}>
      <TextInput
        type="number"
        step={step}
        value={form[key]}
        onChange={set(key)}
        placeholder="0"
      />
    </FormField>
  );

  return (
    <div className="space-y-6">
      {/* ── Location ────────────────────────────────────────────── */}
      <div>
        <SectionHeader icon={<MapPin />} title="Location" />
        <div className="grid grid-cols-2 gap-4">
          <FormField label="District" error={errors.district}>
            <SelectInput
              value={form.district}
              onChange={set('district')}
              options={options.districts}
            />
          </FormField>
          {num('latitude',  'Latitude (°N)',  'e.g. 6.9271')}
          {num('longitude', 'Longitude (°E)', 'e.g. 79.8612')}
          {num('elevation_m', 'Elevation (m)', 'Metres above sea level')}
          <div className="col-span-2">
            {num('distance_to_river_m', 'Distance to Nearest River (m)', 'Google Maps / field measurement')}
          </div>
        </div>
      </div>

      {/* ── Land & Soil ─────────────────────────────────────────── */}
      <div>
        <SectionHeader icon={<Layers />} title="Land & Soil" />
        <div className="grid grid-cols-2 gap-4">
          <FormField label="Land Cover" error={errors.landcover}>
            <SelectInput
              value={form.landcover}
              onChange={set('landcover')}
              options={options.landcovers}
            />
          </FormField>
          <FormField label="Soil Type" error={errors.soil_type}>
            <SelectInput
              value={form.soil_type}
              onChange={set('soil_type')}
              options={options.soil_types}
            />
          </FormField>
        </div>
      </div>

      {/* ── Rainfall & Hydrology ────────────────────────────────── */}
      <div>
        <SectionHeader icon={<Cloud />} title="Rainfall & Hydrology" />
        <div className="grid grid-cols-2 gap-4">
          {num('rainfall_7d_mm',          'Rainfall Last 7 Days (mm)',  'Weather app / station')}
          {num('monthly_rainfall_mm',     'Monthly Rainfall (mm)',       'Weather app / station')}
          {num('rainfall_intensity_mmhr', 'Rainfall Intensity (mm/hr)', 'Peak rate')}
          {num('river_flow_rate_m3s',     'River Flow Rate (m³/s)',      'DMC / irrigation gauge')}
        </div>
      </div>

      {/* ── Historical ──────────────────────────────────────────── */}
      <div>
        <SectionHeader icon={<History />} title="Historical Data" />
        {num('historical_flood_count', 'Past Flood Events at This Location', 'DMC records / community knowledge', 1)}
      </div>

      {/* Submit */}
      <button
  onClick={handleSubmit}
  disabled={loading}
  className="w-full py-3.5 rounded-xl font-semibold text-white flex items-center justify-center gap-2
             bg-gradient-to-r from-blue-600 to-blue-500
             hover:from-blue-700 hover:to-blue-600
             active:scale-[.98] transition-all duration-150 shadow-md
             disabled:opacity-60 disabled:cursor-not-allowed"
>
  {loading
    ? <><Loader2 size={18} className="animate-spin" /> Predicting…</>
    : <><Zap size={18} /> Run Flood Prediction</>
  }
</button>
    </div>
  );
}
