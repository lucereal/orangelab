#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include "secrets.h"

#define LED_PIN    4
#define NUM_LEDS   25
#define BRIGHTNESS 200

#include "effects.h"

const char* SCAN_TOPIC = "token/dock/scan";
const String RESULT_TOPIC = String("token/dock/result/") + String(SCANNER_ID);

PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
CRGB leds[NUM_LEDS];

String lastUID = "";
bool pendingEffect = false;
CRGB pendingColor = CRGB::Black;

void onMQTTMessage(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println("Result: " + message);

  int reasonCode = 0;
  int idx = message.indexOf("\"reason_code\":");
  if (idx >= 0) {
    reasonCode = message.substring(idx + 14).toInt();
  }

  if (reasonCode == 10) {
    pendingColor = CRGB::Green;
  } else if (reasonCode == 1) {
    pendingColor = CRGB(255, 80, 0);  // orange
  } else {
    pendingColor = CRGB::Red;
  }

  pendingEffect = true;
}

void connectMQTT() {
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(onMQTTMessage);
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    String clientId = String("scanner_") + String(SCANNER_ID);
    if (mqtt.connect(clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("connected");
      mqtt.subscribe(RESULT_TOPIC.c_str());
    } else {
      Serial.println("failed, retrying in 2s");
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(9600);

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear(true);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());

  nfc.begin();
  uint32_t versiondata = 0;
  for (int i = 0; i < 5 && !versiondata; i++) {
    versiondata = nfc.getFirmwareVersion();
    if (!versiondata) {
      Serial.println("PN532 not found, retrying...");
      delay(500);
    }
  }
  if (!versiondata) {
    Serial.println("PN532 not found - check wiring and I2C jumpers");
    while (1);
  }
  nfc.SAMConfig();

  connectMQTT();
  Serial.println("Waiting for NFC card...");
}

void loop() {
  if (!mqtt.connected()) {
    connectMQTT();
  }
  mqtt.loop();

  if (pendingEffect) {
    pendingEffect = false;
    flashFade(pendingColor, 250);
  }


  uint8_t uid[7];
  uint8_t uidLength;

  bool found = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 20);

  if (!found) {
    if (lastUID != "") {
      Serial.println("Card removed: " + lastUID);
      lastUID = "";
    }
    return;
  }

  String uidStr = "";
  for (uint8_t i = 0; i < uidLength; i++) {
    if (uid[i] < 0x10) uidStr += "0";
    uidStr += String(uid[i], HEX);
  }
  uidStr.toUpperCase();

  if (uidStr == lastUID) return;

  Serial.println("Card: " + uidStr);
  if (publishUID(uidStr)) {
    lastUID = uidStr;
  }
}

bool publishUID(String uid) {
  if (!mqtt.connected()) {
    Serial.println("MQTT disconnected");
    return false;
  }

  String payload = "{\"uid\":\"" + uid + "\",\"scanner_id\":" + String(SCANNER_ID) + ",\"mac\":\"" + WiFi.macAddress() + "\"}";
  bool ok = mqtt.publish(SCAN_TOPIC, payload.c_str());
  Serial.println("Published: " + payload);
  return ok;
}
