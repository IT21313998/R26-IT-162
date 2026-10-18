"""
mqtt_subscriber.py
Connects to the public MQTT broker (broker.emqx.io)
to receive live rainfall intensity, water cup volume, and fill time from the ESP32 node.

Matches the exact ESP32 topics:
  - smart_irrigation/unit1/waterML
  - smart_irrigation/unit1/rainIntensity
  - smart_irrigation/unit1/fillTime
  - smart_irrigation/unit1/distanceCM
  - smart_irrigation/unit1/valveStatus
  - smart_irrigation/unit1/alert
"""

import json
import sys
import time
import threading
from typing import Callable, Optional, Dict, Any, List
from datetime import datetime

# Fix Windows terminal emoji encoding crash
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    import paho.mqtt.client as mqtt
    HAS_PAHO = True
except ImportError:
    HAS_PAHO = False


def _print(msg: str):
    """Safe print that handles Windows emoji/encoding issues."""
    try:
        print(msg)
    except UnicodeEncodeError:
        # Strip non-ASCII characters and print
        print(msg.encode('ascii', 'replace').decode('ascii'))


class IoTRainSubscriber:
    """
    Subscribes to MQTT broker (broker.emqx.io)
    and receives live rain sensor telemetry matching the ESP32 SIM800L firmware.
    """
    
    DEFAULT_BROKER = "broker.emqx.io"
    DEFAULT_PORT = 1883
    DEFAULT_TOPICS = [
        "smart_irrigation/unit1/#",
        "smart_irrigation/unit1/waterML",
        "smart_irrigation/unit1/rainIntensity",
        "smart_irrigation/unit1/fillTime",
        "smart_irrigation/unit1/distanceCM",
        "smart_irrigation/unit1/valveStatus",
        "smart_irrigation/unit1/alert",
        "Smart Irrigation Hive/#"
    ]
    
    # Physical Calibration: 125ml collection cup
    # 1 ml = 0.1 mm of rainfall (for 100 cm2 funnel area)
    ML_TO_MM_RATIO = 0.1
    
    def __init__(
        self, 
        broker: str = DEFAULT_BROKER, 
        port: int = DEFAULT_PORT, 
        topics: Optional[List[str]] = None,
        on_packet_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        self.broker = broker
        self.port = port
        self.topics = topics or self.DEFAULT_TOPICS
        self.on_packet_callback = on_packet_callback
        
        self.client: Optional[Any] = None
        self.is_connected = False
        
        # State tracking for ESP32 unit1
        self.current_state: Dict[str, Any] = {
            "waterML": 0.0,
            "rain_mm": 0.0,
            "rainIntensity": "LIGHT",
            "fillTimeSeconds": 0,
            "distanceCM": 11.0,
            "valveStatus": "CLOSED",
            "lastAlert": "NONE",
            "last_updated": None,
            "connected": False
        }
        
        self.packet_count = 0

    def start(self):
        """Starts the MQTT listener loop in a background daemon thread."""
        if not HAS_PAHO:
            _print("[WARNING] 'paho-mqtt' library not installed. Run: python -m pip install paho-mqtt")
            return

        client_id = f"PythonRainHub_{int(time.time())}"
        try:
            if hasattr(mqtt, 'CallbackAPIVersion'):
                self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
            else:
                self.client = mqtt.Client(client_id=client_id)
        except Exception:
            self.client = mqtt.Client(client_id=client_id)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        try:
            _print(f"[INFO] Connecting to MQTT broker at {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            _print("[OK] MQTT background listener started!")
        except Exception as e:
            _print(f"[ERROR] Failed to connect to MQTT broker: {e}")

    def stop(self):
        """Stops the MQTT client."""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.is_connected = False
            self.current_state["connected"] = False
            _print("[INFO] MQTT client disconnected.")

    def _on_connect(self, client, userdata, flags, rc, *args):
        if rc == 0 or (hasattr(mqtt, 'MQTT_ERR_SUCCESS') and rc == mqtt.MQTT_ERR_SUCCESS):
            self.is_connected = True
            self.current_state["connected"] = True
            _print(f"[OK] Connected to MQTT Broker ({self.broker}:{self.port})")
            for t in self.topics:
                client.subscribe(t)
                _print(f"   Subscribed: '{t}'")
        else:
            _print(f"[ERROR] MQTT Connection failed with return code: {rc}")

    def _on_disconnect(self, client, userdata, rc, *args):
        self.is_connected = False
        self.current_state["connected"] = False
        _print(f"[WARNING] Disconnected from MQTT broker (code: {rc}). Reconnecting...")

    def _on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload_str = msg.payload.decode('utf-8').strip()
            self.packet_count += 1
            now_iso = datetime.now().isoformat()
            
            # Map topics from ESP32 code
            if topic.endswith("waterML"):
                try:
                    ml = float(payload_str)
                    self.current_state["waterML"] = ml
                    self.current_state["rain_mm"] = round(ml * self.ML_TO_MM_RATIO, 2)
                except ValueError:
                    pass

            elif topic.endswith("rainIntensity"):
                self.current_state["rainIntensity"] = payload_str.upper()

            elif topic.endswith("fillTime"):
                try:
                    self.current_state["fillTimeSeconds"] = int(payload_str)
                except ValueError:
                    pass

            elif topic.endswith("distanceCM"):
                try:
                    self.current_state["distanceCM"] = float(payload_str)
                except ValueError:
                    pass

            elif topic.endswith("valveStatus"):
                self.current_state["valveStatus"] = payload_str.upper()

            elif topic.endswith("alert"):
                self.current_state["lastAlert"] = payload_str
                
            self.current_state["last_updated"] = now_iso
            
            # Construct unified packet for ML fusion engine
            unified_packet = {
                "device_id": "ESP32_SIM800L_UNIT1",
                "timestamp": now_iso,
                "rain": self.current_state["rain_mm"],
                "water_ml": self.current_state["waterML"],
                "rain_intensity": self.current_state["rainIntensity"],
                "fill_time_sec": self.current_state["fillTimeSeconds"],
                "distance_cm": self.current_state["distanceCM"],
                "valve_status": self.current_state["valveStatus"],
                "topic": topic,
                "raw_payload": payload_str
            }
            
            _print(f"[PACKET #{self.packet_count}] {topic} -> {payload_str} | Rain: {self.current_state['rain_mm']} mm")
            
            if self.on_packet_callback:
                self.on_packet_callback(unified_packet)
                
        except Exception as e:
            _print(f"[ERROR] Error parsing MQTT message: {e}")

    def get_latest_state(self) -> Dict[str, Any]:
        """Returns the latest sensor state from ESP32."""
        return self.current_state.copy()


# Backward compatibility alias
HiveMQRainSubscriber = IoTRainSubscriber


if __name__ == '__main__':
    _print("Testing IoT MQTT Subscriber on broker.emqx.io...")
    _print("Waiting for messages from smart_irrigation/unit1/# ...")
    _print("(Make sure your ESP32 is powered on with SIM card inserted)")
    _print("-" * 60)
    sub = IoTRainSubscriber()
    sub.start()
    try:
        time.sleep(30)  # Wait 30 seconds for messages
        state = sub.get_latest_state()
        _print("-" * 60)
        _print(f"Final State: {state}")
        if not state["connected"]:
            _print("[WARNING] ESP32 not connected - no packets received in 30s")
        else:
            _print(f"[OK] Received {sub.packet_count} packets from ESP32")
    finally:
        sub.stop()
