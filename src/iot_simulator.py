"""
iot_simulator.py
Demonstration script simulating an IoT Rain Gauge & Weather Station
transmitting live sensor packets to the IoTRainPredictor engine.
"""

import time
import json
import random
from datetime import datetime, timedelta
import pandas as pd
from iot_predictor import IoTRainPredictor


def simulate_iot_device_stream(csv_sample_path: str, bundle_path: str = 'rain_model_bundle.joblib', num_steps: int = 10):
    """
    Simulates real-time IoT transmissions by streaming recent rows from the dataset.
    """
    print("=" * 60)
    print("  LIVE IoT RAIN SENSOR TRANSMISSION & PREDICTION SIMULATOR")
    print("=" * 60)
    
    # Initialize predictor
    try:
        predictor = IoTRainPredictor(model_bundle_path=bundle_path)
        print(f" Loaded ML Model Bundle from: {bundle_path}")
    except Exception as e:
        print(f" Warning: Could not load {bundle_path} ({e}). Ensure model is trained first.")
        return
        
    # Read sample historical data
    df_raw = pd.read_csv(csv_sample_path, skiprows=3)
    df_raw['time'] = pd.to_datetime(df_raw['time'])
    
    # Preload previous 72 hours to populate buffer
    history_slice = df_raw.iloc[-100:-num_steps].copy()
    predictor.load_historical_buffer(history_slice)
    print(f" Preloaded {len(predictor.buffer)} historical readings into rolling buffer.\n")
    
    # Stream the latest `num_steps` as "Live IoT packets"
    stream_slice = df_raw.iloc[-num_steps:].copy()
    
    for idx, (_, row) in enumerate(stream_slice.iterrows()):
        # Simulate IoT JSON packet
        iot_packet = {
            'device_id': 'ESP32_RAIN_STATION_01',
            'timestamp': row['time'].isoformat(),
            'temperature': float(row['temperature_2m (°C)']),
            'relative_humidity': float(row['relative_humidity_2m (%)']),
            'surface_pressure': float(row['surface_pressure (hPa)']),
            'cloud_cover': float(row['cloud_cover (%)']),
            'rain': float(row['rain (mm)']),
            'wind_speed_10m': float(row.get('wind_speed_10m (km/h)', 10.0)),
            'wind_direction_10m': float(row.get('wind_direction_10m (°)', 45.0))
        }
        
        print(f" [IoT Packet Received] Time: {iot_packet['timestamp']} | Temp: {iot_packet['temperature']}°C | Humidity: {iot_packet['relative_humidity']}% | Rain: {iot_packet['rain']}mm | Pressure: {iot_packet['surface_pressure']}hPa")
        
        # Ingest into predictor
        predictor.add_sensor_reading(iot_packet)
        
        # Generate 1 to 3 Day Forecast
        forecast = predictor.predict_forecast()
        
        print("\n---  UPDATED 1 TO 3-DAY RAIN FORECAST ---")
        for day_key, data in forecast['forecast_horizons'].items():
            print(f"   [{data['horizon_name']}]: Rain: {data['predicted_rainfall_mm']:>5.1f} mm | Prob: {data['rain_probability_pct']:>5.1f}% | Alert: {data['risk_level']}")
        print("-" * 60)
        time.sleep(0.3)  # Brief delay for terminal demonstration


if __name__ == '__main__':
    import os
    sample_csv = 'open-meteo-6.99N79.90E8m (1).csv'
    if os.path.exists(sample_csv):
        simulate_iot_device_stream(sample_csv)
    else:
        print(f"Sample CSV {sample_csv} not found in current directory.")
