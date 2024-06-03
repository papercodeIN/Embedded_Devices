#include <ESP8266WiFi.h>
#include <ModbusIP_ESP8266.h>
#include <FastLED.h>

const char* ssid = "Capgemini_4G";
const char* password = "MN704116";

#define LED_PIN 5 // Change to your LED pin
#define NUM_LEDS 10 // Number of LEDs
#define LED_TYPE WS2812B // LED type
#define COLOR_ORDER GRB // LED color order
#define BRIGHTNESS 5 // LED brightness

CRGB leds[NUM_LEDS];
ModbusIP mb;

void setup() {
  Serial.begin(115200);

  // Set fixed IP address, subnet mask, and gateway
  IPAddress ip(192, 168, 1, 4);
  IPAddress subnet(255, 255, 255, 0);
  IPAddress gateway(192, 168, 1, 1);

  // Connect to WiFi with fixed IP configuration
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Initialize Modbus server
  mb.server(502);

  // Set up LED strip
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);

  // Add 10 holding registers for LED colors
  for (int i = 0; i < NUM_LEDS; i++) {
    mb.addHreg(i, 0); // Initialize all holding registers to zero
  }
}

void loop() {
  mb.task(); // Handle Modbus communication

  // Update LEDs based on holding register values
  for (int i = 0; i < NUM_LEDS; i++) {
    int ledColor = mb.Hreg(i); // Read holding register value
    if (ledColor == 0) {
      leds[i] = CRGB::Black; // Turn off LED
    } else if (ledColor == 1) {
      leds[i] = CRGB::Green; // Set LED to green
    } else if (ledColor == 2) {
      leds[i] = CRGB::Red; // Set LED to red
    } else {
      // Default color if invalid value
      leds[i] = CRGB::White;
    }
  }

  FastLED.show(); // Update LED strip
}
