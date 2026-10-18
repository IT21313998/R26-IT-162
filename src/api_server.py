"""
api_server.py
REST API and MQTT Dispatcher for Student B Partner Model Integration.

Provides endpoints for Student B's Water Level and Dynamic Flood Risk Score (DFRS) model
to fetch 24h, 48h, and 72h rainfall forecasts.
Also receives live HTTP POST telemetry from IoT nodes.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from fastapi import FastAPI, BackgroundTasks, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from fusion_engine import RealTimeDataFusionEngine
from mqtt_subscriber import HiveMQRainSubscriber

# Global fusion engine instance
fusion_engine = RealTimeDataFusionEngine()
mqtt_sub: Optional[HiveMQRainSubscriber] = None


def create_app():
    if not HAS_FASTAPI:
        return None
        
    app = FastAPI(
        title="Kelani River Flood Early Warning - Student A Prediction API",
        description="REST API providing 24h, 48h, and 72h Hyperlocal Rainfall Predictions for Student B's Water Level and DFRS Model.",
        version="1.0.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.on_event("startup")
    def startup_event():
        global mqtt_sub
        print("🚀 Starting MQTT Subscriber for HiveMQ 'Smart Irrigation Hive'...")
        
        def on_mqtt_packet(packet):
            print("⚡ Updating ML forecast with new HiveMQ IoT packet...")
            fusion_engine.process_incoming_iot_packet(packet, fetch_live_api=True)
            
        mqtt_sub = HiveMQRainSubscriber(on_packet_callback=on_mqtt_packet)
        mqtt_sub.start()
        
        # Initial run with current live weather
        fusion_engine.process_incoming_iot_packet({"rain": 0.0, "source": "API Startup Init"})

    @app.on_event("shutdown")
    def shutdown_event():
        if mqtt_sub:
            mqtt_sub.stop()

    @app.get("/")
    def root():
        return {
            "project": "R26-IT-162 SLIIT Flood Early Warning System",
            "component": "Student A - Hyperlocal Rainfall ML Prediction Engine",
            "status": "ONLINE",
            "documentation": "/docs",
            "partner_endpoint": "/api/v1/forecast/latest"
        }

    @app.get("/api/v1/forecast/latest")
    def get_latest_forecast():
        """
        Primary Endpoint for Student B:
        Returns latest 24h, 48h, and 72h rainfall predictions and basin alert levels.
        """
        forecast = fusion_engine.get_latest_forecast()
        if not forecast:
            # Generate fresh forecast on demand
            forecast = fusion_engine.process_incoming_iot_packet({"rain": 0.0})
        return forecast

    @app.post("/api/v1/iot/telemetry")
    def receive_iot_telemetry(payload: Dict[str, Any]):
        """
        Direct HTTP POST Endpoint for ESP32 / IoT nodes to submit rainfall data.
        """
        forecast = fusion_engine.process_incoming_iot_packet(payload, fetch_live_api=True)
        return {
            "status": "RECEIVED_AND_PROCESSED",
            "timestamp": datetime.now().isoformat(),
            "updated_forecast": forecast["student_b_inputs"]
        }

    @app.get("/api/v1/weather/ambient")
    def get_ambient_weather():
        """
        Returns live Open-Meteo atmospheric readings for Kelani River Basin.
        """
        return fusion_engine.weather_api.fetch_current_weather(force_refresh=True)

    @app.post("/api/v1/integrated/flood-risk")
    def compute_integrated_flood_risk(community_params: Optional[Dict[str, Any]] = None):
        """
        Integrated End-to-End Pipeline Endpoint:
        Takes latest multi-horizon rainfall forecasts from Student A, fuses with
        community spatial parameters, and executes Student B's Two-Stage XGBoost
        models to return Flood Probability, Risk Score, Arrival Time, and Water Height.
        """
        from integration_bridge import PartnerFloodRiskPredictor
        predictor = PartnerFloodRiskPredictor()
        
        latest_fc = fusion_engine.get_latest_forecast()
        if not latest_fc:
            latest_fc = fusion_engine.process_incoming_iot_packet({"rain": 0.0})
            
        return predictor.predict_from_student_a_forecast(
            student_a_payload=latest_fc,
            location_params=community_params
        )

    return app



# CLI runner
if __name__ == "__main__":
    if HAS_FASTAPI:
        app = create_app()
        print("Starting FastAPI Server on http://0.0.0.0:8000 ...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("FastAPI / Uvicorn not installed. Install with `pip install fastapi uvicorn`")
