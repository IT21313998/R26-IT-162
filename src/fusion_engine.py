"""
fusion_engine.py
Real-time Data Fusion & Multi-Horizon Inference Engine.

Fuses live IoT rainfall measurements (from HiveMQ or sensor)
with live atmospheric weather variables (from Open-Meteo API)
to generate continuous 24h, 48h, and 72h rainfall forecasts.
Formats the outputs specifically for Student B's Water Level / DFRS Model.
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

import pandas as pd
import numpy as np

# Internal modules
from live_weather_api import LiveWeatherAPI
from iot_predictor import IoTRainPredictor
from mqtt_subscriber import IoTRainSubscriber


class RealTimeDataFusionEngine:
    """
    Coordinates live IoT rain gauge ingestion, Open-Meteo live API atmospheric data fetching,
    and multi-horizon ML predictions (24h, 48h, 72h).
    """
    
    def __init__(
        self,
        model_bundle_path: str = 'rain_model_bundle.joblib',
        historical_csv_path: Optional[str] = 'open-meteo-6.99N79.90E8m (1).csv',
        lat: float = 6.9947,
        lon: float = 79.8987
    ):
        self.model_bundle_path = model_bundle_path
        self.weather_api = LiveWeatherAPI(lat=lat, lon=lon)
        self.predictor = IoTRainPredictor()
        
        # Load model if bundle file exists
        if os.path.exists(model_bundle_path):
            self.predictor.load_bundle(model_bundle_path)
            print(f"[OK] Loaded ML Model Bundle from: {model_bundle_path}")
        else:
            print(f"[NOTE] '{model_bundle_path}' not found yet. Using physics fallback.")

        # Prepopulate historical buffer
        if historical_csv_path and os.path.exists(historical_csv_path):
            try:
                df_hist = pd.read_csv(historical_csv_path, skiprows=3)
                self.predictor.load_historical_buffer(df_hist.tail(100))
                print(f"[OK] Preloaded {len(self.predictor.buffer)} historical records into rolling buffer.")
            except Exception as e:
                print(f"[WARNING] Failed to preload history: {e}")

        # Start live MQTT subscriber for ESP32 telemetry (broker.emqx.io)
        self.mqtt_subscriber = IoTRainSubscriber(
            on_packet_callback=self._on_iot_packet
        )
        try:
            self.mqtt_subscriber.start()
        except Exception as e:
            print(f"[WARNING] Could not start MQTT subscriber: {e}")
                
        self.latest_forecast: Optional[Dict[str, Any]] = None
        self.last_iot_reading: Optional[Dict[str, Any]] = None
        self.last_api_weather: Optional[Dict[str, Any]] = None

    def _on_iot_packet(self, packet: Dict[str, Any]):
        """Called automatically when a new MQTT packet arrives from ESP32."""
        self.last_iot_reading = packet



    def process_incoming_iot_packet(
        self, 
        iot_packet: Dict[str, Any], 
        fetch_live_api: bool = True
    ) -> Dict[str, Any]:
        """
        Fuses a live IoT packet with live atmospheric weather data.
        
        Args:
            iot_packet: Dictionary with at least {'rain': float} from ESP32.
            fetch_live_api: Whether to query Open-Meteo API for real-time ambient parameters.
            
        Returns:
            Formatted multi-day prediction dictionary for Student A & Student B.
        """
        self.last_iot_reading = iot_packet
        
        # Extract rainfall from IoT device
        measured_rain = float(iot_packet.get('rain', iot_packet.get('rainfall_mm', 0.0)))
        
        # Fetch ambient atmospheric conditions from Open-Meteo live API
        if fetch_live_api:
            api_weather = self.weather_api.fetch_current_weather()
            self.last_api_weather = api_weather
        else:
            api_weather = self.last_api_weather or self.weather_api.fetch_current_weather()
            
        # Merge: Prioritize IoT rain gauge for 'rain', and use API for atmospheric variables
        # If IoT packet provides temperature/humidity (e.g. from DHT22), use those; otherwise API
        fused_reading = {
            'timestamp': iot_packet.get('timestamp', datetime.now().isoformat()),
            'rain': measured_rain,  # Hyperlocal IoT measurement
            'temperature': float(iot_packet.get('temperature', api_weather['temperature'])),
            'relative_humidity': float(iot_packet.get('relative_humidity', api_weather['relative_humidity'])),
            'surface_pressure': float(iot_packet.get('surface_pressure', api_weather['surface_pressure'])),
            'cloud_cover': float(iot_packet.get('cloud_cover', api_weather['cloud_cover'])),
            'wind_speed_10m': float(iot_packet.get('wind_speed_10m', api_weather['wind_speed_10m'])),
            'wind_direction_10m': float(iot_packet.get('wind_direction_10m', api_weather['wind_direction_10m']))
        }
        
        # Ingest into sliding window buffer
        self.predictor.add_sensor_reading(fused_reading)
        
        # Execute ML multi-horizon prediction
        raw_forecast = self.predictor.predict_forecast()
        
        # Format standardized response for Student B's Model & Decision Support System
        formatted_payload = self._format_student_b_payload(fused_reading, raw_forecast)
        self.latest_forecast = formatted_payload
        return formatted_payload

    def _format_student_b_payload(
        self, 
        current_state: Dict[str, Any], 
        raw_forecast: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a clean JSON schema explicitly tailored for Student B's
        Distance-Based Dynamic Flood Risk Personalization (DFRS) and Water Level Model.
        """
        now = datetime.now()
        horizons = raw_forecast.get('forecast_horizons', {})
        
        day1 = horizons.get('day_1', {})
        day2 = horizons.get('day_2', {})
        day3 = horizons.get('day_3', {})
        
        # Cumulative 72h total rainfall
        tot_72h = (
            day1.get('predicted_rainfall_mm', 0.0) +
            day2.get('predicted_rainfall_mm', 0.0) +
            day3.get('predicted_rainfall_mm', 0.0)
        )
        
        # Overall flood warning tier for Kelani river basin
        if tot_72h > 150.0 or day1.get('predicted_rainfall_mm', 0.0) > 75.0:
            basin_alert_level = "MAJOR_FLOOD_WARNING"
            basin_alert_sinhala = "මහා ගංවතුර අනතුරු ඇඟවීම"
            basin_alert_tamil = "பெரும் வெள்ள எச்சரிக்கை"
            alert_color = "#D32F2F"
        elif tot_72h > 75.0 or day1.get('predicted_rainfall_mm', 0.0) > 35.0:
            basin_alert_level = "MINOR_FLOOD_ALERT"
            basin_alert_sinhala = "සුළු ගංවතුර අනතුරු ඇඟවීම"
            basin_alert_tamil = "சிறிய வெள்ள எச்சரிக்கை"
            alert_color = "#F57C00"
        elif tot_72h > 25.0 or day1.get('predicted_rainfall_mm', 0.0) > 10.0:
            basin_alert_level = "ALERT_WATCH"
            basin_alert_sinhala = "විමසිලිමත් මට්ටම"
            basin_alert_tamil = "கண்காணிப்பு நிலை"
            alert_color = "#FBC02D"
        else:
            basin_alert_level = "NORMAL"
            basin_alert_sinhala = "සාමාන්‍ය මට්ටම"
            basin_alert_tamil = "சாதாரண நிலை"
            alert_color = "#388E3C"
            
        payload = {
            "status": "SUCCESS",
            "project_id": "R26-IT-162",
            "module": "Student_A_Hyperlocal_Rainfall_Prediction",
            "generated_at": now.isoformat(),
            "river_basin": "Kelani Ganga (RB 01)",
            "telemetry_fusion": {
                "iot_rain_gauge_mm": current_state['rain'],
                "ambient_temperature_c": current_state['temperature'],
                "relative_humidity_pct": current_state['relative_humidity'],
                "surface_pressure_hpa": current_state['surface_pressure'],
                "cloud_cover_pct": current_state['cloud_cover'],
                "wind_speed_kmh": current_state['wind_speed_10m'],
                "data_sources": ["Hyperlocal ESP32 IoT Rain Sensor", "Open-Meteo Live API"]
            },
            "student_b_inputs": {
                "forecast_24h_mm": day1.get('predicted_rainfall_mm', 0.0),
                "forecast_48h_mm": day2.get('predicted_rainfall_mm', 0.0),
                "forecast_72h_mm": day3.get('predicted_rainfall_mm', 0.0),
                "cumulative_72h_mm": round(tot_72h, 2),
                "rain_probability_24h": day1.get('rain_probability_pct', 0.0),
                "rain_probability_48h": day2.get('rain_probability_pct', 0.0),
                "rain_probability_72h": day3.get('rain_probability_pct', 0.0)
            },
            "flood_risk_classification": {
                "basin_alert_level": basin_alert_level,
                "alert_color_hex": alert_color,
                "multilingual_summary": {
                    "en": f"Forecast indicates {day1.get('predicted_rainfall_mm', 0.0)} mm in next 24h ({basin_alert_level}).",
                    "si": f"ඉදිරි පැය 24 තුළ වර්ෂාපතනය මි.මී. {day1.get('predicted_rainfall_mm', 0.0)} ක් පුරෝකථනය කෙරේ ({basin_alert_sinhala}).",
                    "ta": f"அடுத்த 24 மணித்தியாலங்களில் {day1.get('predicted_rainfall_mm', 0.0)} மி.மீ மழை எதிர்பார்க்கப்படுகிறது ({basin_alert_tamil})."
                }
            }
        }
        
        return payload

    def get_latest_forecast(self) -> Optional[Dict[str, Any]]:
        """Returns the most recent prediction payload."""
        return self.latest_forecast
