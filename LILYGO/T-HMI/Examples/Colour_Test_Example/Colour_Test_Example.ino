#include "pins.h"
#include "Arduino.h"
#include "TFT_eSPI.h"
#include "logo.h"

TFT_eSPI tft = TFT_eSPI();
#define WAIT 1000

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

void displayText(const char* header, bool invert) {
  tft.invertDisplay(invert);
  tft.fillScreen(TFT_BLACK);
  tft.drawRect(0, 0, tft.width(), tft.height(), TFT_GREEN);

  tft.setCursor(0, 4, 4);

  tft.setTextColor(TFT_WHITE);
  tft.println(header);
  tft.println(" White text");

  tft.setTextColor(TFT_RED);
  tft.println(" Red text");

  tft.setTextColor(TFT_GREEN);
  tft.println(" Green text");

  tft.setTextColor(TFT_BLUE);
  tft.println(" Blue text");

  delay(5000);
}

void setup() {
  pinMode(PWR_EN_PIN, OUTPUT);
  digitalWrite(PWR_EN_PIN, HIGH);

  Serial.begin(115200);
  Serial.println("Hello T-HMI");

  tft.begin();
  tft.setRotation(0);
  tft.setSwapBytes(true);
  tft.pushImage(0, 0, 240, 320, (uint16_t*)gImage_logo);

  setBrightness(16);

  delay(3000);

  tft.fillScreen(TFT_BLACK);
  tft.drawRect(0, 0, tft.width(), tft.height(), TFT_GREEN);

  tft.setCursor(0, 4, 4);

  tft.setTextColor(TFT_WHITE);
  tft.println(" Initialised default\n");
  tft.println(" White text");

  tft.setTextColor(TFT_RED);
  tft.println(" Red text");

  tft.setTextColor(TFT_GREEN);
  tft.println(" Green text");

  tft.setTextColor(TFT_BLUE);
  tft.println(" Blue text");

  delay(5000);
}

void loop() {
  displayText("Invert OFF\n", false);
  displayText("Invert ON\n", true);
}
