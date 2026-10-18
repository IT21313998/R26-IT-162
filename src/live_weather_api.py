"""
live_weather_api.py
Fetches real-time atmospheric variables from the Open-Meteo Live API
for Kelani River Basin coordinates (Colombo / Western Province, Sri Lanka).

No API key required (100% free and open).
"""

import time
import requests
from typing import Dict, Any, Optional
from datetime import datetime


class LiveWeatherAPI:
    """
    Fetches real-time ambient weather variables (temperature, surface pressure,
    relative humidity, cloud cover, wind speed, wind direction) for Kelani River Basin.
    """
    
    # Kelani River Basin default coordinates (Colombo / River Mouth)
    DEFAULT_LAT = 6.9947
    DEFAULT_LON = 79.8987
    
    def __init__(self, lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON, cache_ttl_seconds: int = 600):
        self.lat = lat
        self.lon = lon
        self.cache_ttl = cache_ttl_seconds
        self._last_fetch_time: Optional[float] = None
        self._cached_weather: Optional[Dict[str, Any]] = None

    def fetch_current_weather(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Retrieves current atmospheric readings from Open-Meteo API.
        Uses in-memory caching to prevent excessive API calls while keeping data fresh.
        """
        now = time.time()
        if not force_refresh and self._cached_weather is not None and self._last_fetch_time is not None:
            if (now - self._last_fetch_time) < self.cache_ttl:
                return self._cached_weather
                
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "surface_pressure",
                "cloud_cover",
                "wind_speed_10m",
                "wind_direction_10m",
                "precipitation"
            ],
            "timezone": "Asia/Colombo"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            curr = data.get("current", {})
            
            weather_data = {
                "timestamp": curr.get("time", datetime.now().isoformat()),
                "temperature": float(curr.get("temperature_2m", 28.0)),
                "relative_humidity": float(curr.get("relative_humidity_2m", 80.0)),
                "surface_pressure": float(curr.get("surface_pressure", 1010.0)),
                "cloud_cover": float(curr.get("cloud_cover", 60.0)),
                "wind_speed_10m": float(curr.get("wind_speed_10m", 12.0)),
                "wind_direction_10m": float(curr.get("wind_direction_10m", 225.0)),
                "api_rain_fallback": float(curr.get("precipitation", 0.0)),
                "location": {
                    "latitude": self.lat,
                    "longitude": self.lon,
                    "basin": "Kelani Ganga River Basin (Sri Lanka)"
                },
                "source": "Open-Meteo Live API"
            }
            
            self._cached_weather = weather_data
            self._last_fetch_time = now
            return weather_data
            
        except Exception as e:
            # Fallback to realistic tropical climatological defaults if offline
            print(f"⚠️ Warning: Failed to fetch live Open-Meteo weather ({e}). Using default tropical baseline.")
            if self._cached_weather:
                return self._cached_weather
                
            return {
                "timestamp": datetime.now().isoformat(),
                "temperature": 28.0,
                "relative_humidity": 82.0,
                "surface_pressure": 1009.5,
                "cloud_cover": 75.0,
                "wind_speed_10m": 14.0,
                "wind_direction_10m": 230.0,
                "api_rain_fallback": 0.0,
                "location": {
                    "latitude": self.lat,
                    "longitude": self.lon,
                    "basin": "Kelani Ganga River Basin (Default Fallback)"
                },
                "source": "Climatological Fallback"
            }


if __name__ == "__main__":
    api = LiveWeatherAPI()
    print("Testing Open-Meteo Live Weather Fetch for Kelani Basin:")
    data = api.fetch_current_weather()
    for k, v in data.items():
        print(f"  {k}: {v}")
