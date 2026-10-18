/*
 * esp32_rain_hivemq.ino
 * 
 * SLIIT Research Project (R26-IT-162) - Student A
 * Hyperlocal IoT Rain Gauge Node for Kelani River Basin Flood Early Warning
 * 
 * Hardware:
 *   - ESP32 Development Board (e.g. NodeMCU ESP32 / WROOM-32)
 *   - Tipping Bucket Rain Gauge Sensor (Connected to GPIO 4 with pullup)
 *   - Optional: DHT22 / BME280 Temperature & Humidity Sensor (GPIO 15)
 * 
 * Communication:
 *   - Broker: broker.hivemq.com (Port 1883, Public Free Broker)
 *   - Topic:  "Smart Irrigation Hive/data"
 * 
 * Libraries Required (install via Arduino Library Manager):
 *   - PubSubClient by Nick O'Leary
 *   - ArduinoJson by Benoit Blanchon (v6 or v7)
 *   - DHT sensor library by Adafruit (optional)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ==========================================
// 1. WiFi & MQTT Configuration
// ==========================================
const char* ssid        = "YOUR_WIFI_SSID";
const char* password    = "YOUR_WIFI_PASSWORD";

const char* mqtt_broker = "broker.hivemq.com";
const int   mqtt_port   = 1883;
const char* mqtt_topic  = "Smart Irrigation Hive/data";
const char* device_id   = "ESP32_KELANI_NODE_01";

// ==========================================
// 2. Hardware Pin Definitions & Calibration
// ==========================================
#define RAIN_PIN            4      // GPIO connected to reed switch of tipping bucket
#define RAIN_CALIBRATION_MM 0.2    // Rainfall per tip in mm (standard tipping bucket: 0.2mm)
#define SEND_INTERVAL_MS    30000  // Transmit interval: 30 seconds for test, 900000ms (15min) for field

// Volatile variables for interrupt
volatile unsigned long tipCount = 0;
volatile unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 100; // 100ms debounce filter

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastSendTime = 0;

// Interrupt Service Routine (ISR) triggered on every bucket tip
void IRAM_ATTR countRainTip() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTime) > debounceDelay) {
    tipCount++;
    lastDebounceTime = currentTime;
  }
}

// ==========================================
// 3. Setup WiFi Connection
// ==========================================
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 30) {
    delay(500);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi connection failed. Retrying in loop...");
  }
}

// ==========================================
// 4. MQTT Reconnect Loop
// ==========================================
void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Attempting HiveMQ MQTT connection... ");
    String clientId = "ESP32RainClient-" + String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("CONNECTED to HiveMQ!");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

// ==========================================
// 5. Main Setup
// ==========================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("==============================================");
  Serial.println(" ESP32 Rain Gauge Node - Kelani Basin Project");
  Serial.println("==============================================");

  // Configure tipping bucket interrupt
  pinMode(RAIN_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(RAIN_PIN), countRainTip, FALLING);

  setup_wifi();
  client.setServer(mqtt_broker, mqtt_port);
}

// ==========================================
// 6. Main Loop
// ==========================================
void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    setup_wifi();
  }

  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastSendTime > SEND_INTERVAL_MS) {
    lastSendTime = now;

    // Safely retrieve and reset tip count
    noInterrupts();
    unsigned long currentTips = tipCount;
    tipCount = 0; // Reset for next transmission window
    interrupts();

    // Calculate rainfall in millimeters
    float rainfall_mm = currentTips * RAIN_CALIBRATION_MM;

    // Construct JSON Payload
    StaticJsonDocument<256> doc;
    doc["device_id"]   = device_id;
    doc["rainfall_mm"] = rainfall_mm;
    doc["tip_count"]   = currentTips;
    doc["uptime_sec"]  = now / 1000;
    doc["status"]      = "OK";

    char jsonBuffer[256];
    serializeJson(doc, jsonBuffer);

    // Publish to HiveMQ topic
    Serial.print("Publishing to HiveMQ Topic [");
    Serial.print(mqtt_topic);
    Serial.print("]: ");
    Serial.println(jsonBuffer);

    boolean success = client.publish(mqtt_topic, jsonBuffer);
    if (success) {
      Serial.println("Packet successfully transmitted to HiveMQ!");
    } else {
      Serial.println("Packet publish failed!");
    }
  }
}
