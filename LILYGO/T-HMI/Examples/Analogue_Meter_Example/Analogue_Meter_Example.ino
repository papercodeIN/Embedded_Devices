#include <TFT_eSPI.h>     // Hardware-specific library
#include <TFT_eWidget.h>  // Widget library
#include "pins.h"

// Initialize TFT display and widgets
TFT_eSPI tft = TFT_eSPI();
MeterWidget amps = MeterWidget(&tft);
MeterWidget volts = MeterWidget(&tft);

#define LOOP_PERIOD 35  // Display updates every 35 ms

// Brightness control
void setBrightness(uint8_t value) {
  static uint8_t steps = 16;
  static uint8_t _brightness = 0;

  if (_brightness == value) return;

  if (value > steps) value = steps;
  if (value == 0) {
    digitalWrite(BK_LIGHT_PIN, 0);
    delay(3);
    _brightness = 0;
    return;
  }
  if (_brightness == 0) {
    digitalWrite(BK_LIGHT_PIN, 1);
    _brightness = steps;
    delayMicroseconds(30);
  }

  int from = steps - _brightness;
  int to = steps - value;
  int num = (steps + to - from) % steps;

  for (int i = 0; i < num; i++) {
    digitalWrite(BK_LIGHT_PIN, 0);
    digitalWrite(BK_LIGHT_PIN, 1);
  }
  _brightness = value;
}

// Map value function
float mapValue(float ip, float ipmin, float ipmax, float tomin, float tomax) {
  return tomin + (((tomax - tomin) * (ip - ipmin)) / (ipmax - ipmin));
}

void setup() {
  pinMode(PWR_EN_PIN, OUTPUT);
  digitalWrite(PWR_EN_PIN, HIGH);

  Serial.begin(115200);
  Serial.println("Initializing TFT Display");

  // Initialize TFT display
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(TFT_BLACK); // Set background to black
  tft.setSwapBytes(true);

  setBrightness(16);

  // Add padding for centering the first gauge
  int padding = 20;

  // Draw the first meter (Amps) to occupy the top half of the screen, centered vertically
  amps.setZones(75, 100, 50, 75, 25, 50, 0, 25); // Define color zones
  amps.analogMeter(0, padding, 3.0, "Amps", "0", "0.75", "1.5", "2.25", "3.0");

  // Draw the second meter (Volts) to occupy the bottom half of the screen
  volts.setZones(0, 100, 25, 75, 0, 0, 40, 60); // Define color zones
  volts.analogMeter(0, 180, 12.0, "Volts", "0", "3", "6", "9", "12");
}

void loop() {
  static int d = 0;
  static uint32_t updateTime = 0;

  if (millis() - updateTime >= LOOP_PERIOD) {
    updateTime = millis();

    d += 4;
    if (d > 360) d = 0;

    // Sine wave for testing, range 0 - 100
    float value = 50.0 + 50.0 * sin(d * 0.0174532925);

    // Update meters
    float current = mapValue(value, 0.0, 100.0, 0.0, 3.0);  // Adjusted range for "Amps" meter
    amps.updateNeedle(current, 0);

    float voltage = mapValue(value, 0.0, 100.0, 0.0, 12.0); // Adjusted range for "Volts" meter
    volts.updateNeedle(voltage, 0);
  }
}
