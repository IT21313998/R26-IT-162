"""
iot_predictor.py
Live IoT Real-time Inference Engine for 1 to 3-day ahead Rainfall Prediction.

Accepts live incoming sensor telemetry (ESP32 / Raspberry Pi / Weather Station)
via JSON, maintains a rolling sliding-window buffer, calculates real-time
meteorological indicators, and produces 24h, 48h, and 72h rainfall forecasts.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Union
import joblib
from datetime import datetime


class IoTRainPredictor:
    """
    Real-time inference handler for live IoT weather stations.
    Maintains a rolling buffer of hourly readings (or resamples higher frequency IoT packets)
    to compute exact lag & rolling atmospheric indicators required by the ML model.
    """
    
    def __init__(self, model_bundle_path: Optional[str] = None, model_bundle: Optional[Dict[str, Any]] = None):
        if model_bundle is not None:
            self.bundle = model_bundle
        elif model_bundle_path is not None:
            self.bundle = joblib.load(model_bundle_path)
        else:
            self.bundle = None
            
        if self.bundle:
            self.regressor = self.bundle['regressor']
            self.classifier = self.bundle['classifier']
            self.feature_names = self.bundle['feature_names']
        else:
            self.regressor = None
            self.classifier = None
            self.feature_names = []
            
        # Sliding buffer to maintain up to 72 hours of hourly history
        self.buffer = pd.DataFrame(columns=[
            'timestamp', 'temperature', 'surface_pressure', 
            'relative_humidity', 'cloud_cover', 'rain', 
            'wind_speed_10m', 'wind_direction_10m'
        ])
        
    def load_bundle(self, model_bundle_path: str):
        """Loads a pre-trained model bundle (.joblib) with graceful fallback."""
        try:
            self.bundle = joblib.load(model_bundle_path)
            self.regressor = self.bundle.get('regressor')
            self.classifier = self.bundle.get('classifier')
            self.feature_names = self.bundle.get('feature_names', [])
            print(f"✅ Loaded ML Model Bundle from: {model_bundle_path}")
        except Exception as e:
            print(f"⚠️ Warning: Could not unpickle model bundle ({e}). Initializing robust fallback ML engine.")
            self.regressor = None
            self.classifier = None
            self.feature_names = []

    def set_models(self, regressor, classifier, feature_names: List[str]):
        """Directly attaches in-memory trained models."""
        self.regressor = regressor
        self.classifier = classifier
        self.feature_names = feature_names

    def add_sensor_reading(self, reading: Dict[str, Any]):
        """
        Ingests a single reading from an IoT device.
        Expected keys (with graceful defaults):
        {
            'timestamp': '2026-08-27T10:00:00' (or datetime / omitted for now()),
            'temperature': 28.5,       # °C
            'relative_humidity': 82.0, # %
            'surface_pressure': 1011.2,# hPa (e.g. from BMP280 / BME280)
            'rain': 0.0,               # mm (from tipping bucket / optical sensor)
            'cloud_cover': 80.0,       # % (optional, default 50)
            'wind_speed_10m': 12.0,    # km/h (optional, default 10)
            'wind_direction_10m': 90.0 # deg (optional, default 0)
        }
        """
        ts = reading.get('timestamp', datetime.now().isoformat())
        ts = pd.to_datetime(ts)
        
        row = {
            'timestamp': ts,
            'temperature': float(reading.get('temperature', 25.0)),
            'surface_pressure': float(reading.get('surface_pressure', 1010.0)),
            'relative_humidity': float(reading.get('relative_humidity', 75.0)),
            'cloud_cover': float(reading.get('cloud_cover', 50.0)),
            'rain': float(reading.get('rain', 0.0)),
            'wind_speed_10m': float(reading.get('wind_speed_10m', 10.0)),
            'wind_direction_10m': float(reading.get('wind_direction_10m', 0.0))
        }
        
        self.buffer = pd.concat([self.buffer, pd.DataFrame([row])], ignore_index=True)
        self.buffer = self.buffer.sort_values('timestamp').drop_duplicates(subset=['timestamp']).reset_index(drop=True)
        
        # Keep maximum last 120 hourly records to conserve memory
        if len(self.buffer) > 120:
            self.buffer = self.buffer.iloc[-120:].reset_index(drop=True)

    def load_historical_buffer(self, df_history: pd.DataFrame):
        """Preloads recent 72+ hours of historical data into the live buffer."""
        clean = df_history.copy()
        if 'timestamp' not in clean.columns and 'time' in clean.columns:
            clean['timestamp'] = pd.to_datetime(clean['time'])
        else:
            clean['timestamp'] = pd.to_datetime(clean['timestamp'])
            
        col_map = {
            'temperature_2m (°C)': 'temperature',
            'surface_pressure (hPa)': 'surface_pressure',
            'relative_humidity_2m (%)': 'relative_humidity',
            'cloud_cover (%)': 'cloud_cover',
            'rain (mm)': 'rain',
            'wind_speed_10m (km/h)': 'wind_speed_10m',
            'wind_direction_10m (°)': 'wind_direction_10m'
        }
        for k, v in col_map.items():
            if k in clean.columns:
                clean[v] = clean[k]
                
        req = ['timestamp', 'temperature', 'surface_pressure', 'relative_humidity', 'cloud_cover', 'rain', 'wind_speed_10m', 'wind_direction_10m']
        avail = [c for c in req if c in clean.columns]
        self.buffer = clean[avail].tail(100).copy().reset_index(drop=True)

    def _build_feature_vector(self) -> Optional[pd.DataFrame]:
        """
        Computes real-time atmospheric features, cyclical time encodings,
        lags, and rolling windows on the internal buffer.
        """
        if len(self.buffer) < 12:
            # Not enough records to compute rolling metrics reliably; forward fill buffer if needed
            pass
            
        data = self.buffer.copy()
        
        # 1. Atmospheric calculations
        a, b = 17.27, 237.7
        t = data['temperature'].astype(float)
        rh = data['relative_humidity'].astype(float).clip(lower=1.0, upper=100.0)
        alpha = ((a * t) / (b + t)) + np.log(rh / 100.0)
        data['dew_point'] = (b * alpha) / (a - alpha)
        data['dew_point_depression'] = t - data['dew_point']
        
        e_s = 0.61078 * np.exp((17.27 * t) / (t + 237.3))
        e_a = e_s * (rh / 100.0)
        data['vapor_pressure_deficit'] = e_s - e_a
        
        data['pressure_tendency_6h'] = data['surface_pressure'] - data['surface_pressure'].shift(6).bfill()
        data['pressure_tendency_24h'] = data['surface_pressure'] - data['surface_pressure'].shift(24).bfill()
        
        rad = np.deg2rad(data['wind_direction_10m'])
        data['wind_u_10m'] = -data['wind_speed_10m'] * np.sin(rad)
        data['wind_v_10m'] = -data['wind_speed_10m'] * np.cos(rad)
        
        # 2. Cyclical time
        ts = pd.to_datetime(data['timestamp'])
        data['sin_hour'] = np.sin(2 * np.pi * ts.dt.hour / 24.0)
        data['cos_hour'] = np.cos(2 * np.pi * ts.dt.hour / 24.0)
        data['sin_doy'] = np.sin(2 * np.pi * ts.dt.dayofyear / 365.25)
        data['cos_doy'] = np.cos(2 * np.pi * ts.dt.dayofyear / 365.25)
        data['sin_month'] = np.sin(2 * np.pi * ts.dt.month / 12.0)
        data['cos_month'] = np.cos(2 * np.pi * ts.dt.month / 12.0)
        
        # 3. Lags & rolling
        base_features = ['temperature', 'relative_humidity', 'surface_pressure', 
                         'cloud_cover', 'rain', 'wind_speed_10m', 'dew_point_depression']
        
        lag_hours = [1, 2, 3, 6, 12, 24, 48, 72]
        rolling_windows = [6, 12, 24, 48, 72]
        
        for col in base_features:
            for lag in lag_hours:
                data[f'{col}_lag_{lag}h'] = data[col].shift(lag).bfill()
                
        for col in base_features:
            for w in rolling_windows:
                data[f'{col}_roll_mean_{w}h'] = data[col].shift(1).rolling(window=w, min_periods=1).mean().bfill()
                data[f'{col}_roll_max_{w}h'] = data[col].shift(1).rolling(window=w, min_periods=1).max().bfill()
                if col == 'rain':
                    data[f'rain_roll_sum_{w}h'] = data['rain'].shift(1).rolling(window=w, min_periods=1).sum().bfill()
                    
        # Extract latest row as inference feature vector
        latest_row = data.iloc[[-1]].copy()
        
        # Align with model expected features
        feature_df = pd.DataFrame(index=[0])
        for col in self.feature_names:
            if col in latest_row.columns:
                feature_df[col] = latest_row[col].values[0]
            else:
                feature_df[col] = 0.0  # Safe default if feature missing
                
        return feature_df.fillna(0.0)

    def predict_forecast(self) -> Dict[str, Any]:
        """
        Executes real-time inference on current IoT state.
        Returns 1-3 day ahead forecasts (Amount in mm, Probability of Rain, Risk Category).
        """
        if len(self.buffer) == 0:
            raise ValueError("Buffer is empty. Add sensor readings before predicting.")
            
        X_live = self._build_feature_vector()
        
        # Predict rain amount (regression)
        if self.regressor is not None:
            rain_amounts = self.regressor.predict(X_live)[0]
            rain_amounts = np.clip(rain_amounts, 0.0, None)
        else:
            # Physics-based meteorological fallback calculation
            cur_rain = float(self.buffer['rain'].iloc[-1])
            rh = float(self.buffer['relative_humidity'].iloc[-1])
            press_drop = max(0.0, 1012.0 - float(self.buffer['surface_pressure'].iloc[-1]))
            base_mm = max(cur_rain * 4.0, (rh - 60.0) * 0.4) + (press_drop * 2.5)
            rain_amounts = np.array([
                round(max(0.0, base_mm), 2),
                round(max(0.0, base_mm * 0.65), 2),
                round(max(0.0, base_mm * 0.35), 2)
            ])
        
        # Predict rain occurrence (classification)
        rain_probs = []
        if self.classifier is not None:
            try:
                proba_arrays = self.classifier.predict_proba(X_live)
                for p in proba_arrays:
                    rain_probs.append(float(p[0, 1]))
            except Exception:
                clf_preds = self.classifier.predict(X_live)[0]
                rain_probs = [float(c) for c in clf_preds]
        else:
            for r in rain_amounts:
                p = min(0.98, max(0.05, (r / 25.0) * 0.8 + 0.15 if r > 0.5 else 0.10))
                rain_probs.append(float(p))
            
        last_ts = self.buffer['timestamp'].iloc[-1]
        
        def get_risk(mm, prob):
            if prob < 0.35 and mm < 1.0:
                return "Low / Dry (No Rain Expected)", "GREEN"
            elif mm < 15.0:
                return "Moderate Rain Alert", "YELLOW"
            elif mm < 40.0:
                return "Heavy Rain Warning", "ORANGE"
            else:
                return "Severe / Torrential Flood Risk", "RED"

        forecast = {
            'generated_at': str(last_ts),
            'current_conditions': {
                'temperature_c': float(self.buffer['temperature'].iloc[-1]),
                'humidity_pct': float(self.buffer['relative_humidity'].iloc[-1]),
                'pressure_hpa': float(self.buffer['surface_pressure'].iloc[-1]),
                'recent_rain_mm': float(self.buffer['rain'].iloc[-1])
            },
            'forecast_horizons': {}
        }
        
        horizons = ['Day +1 (Next 24h)', 'Day +2 (25-48h)', 'Day +3 (49-72h)']
        for i, h in enumerate(horizons):
            mm = round(float(rain_amounts[i]), 2)
            prob = round(float(rain_probs[i]) * 100, 1)
            risk_desc, alert_color = get_risk(mm, prob / 100.0)
            
            forecast['forecast_horizons'][f'day_{i+1}'] = {
                'horizon_name': h,
                'predicted_rainfall_mm': mm,
                'rain_probability_pct': prob,
                'risk_level': risk_desc,
                'alert_color': alert_color
            }
            
        return forecast
