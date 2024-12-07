#include <XPT2046_Touchscreen.h>
#include <SPI.h>

// MOSI=11, MISO=12, SCK=13

#define CS_PIN  39
#define MOSI_PIN 11  // Define your custom MOSI pin
#define MISO_PIN 13  // Define your custom MISO pin
#define SCK_PIN  12  // Define your custom SCK pin

// The TIRQ interrupt signal must be used for this example.
#define TIRQ_PIN  42
XPT2046_Touchscreen ts(CS_PIN,TIRQ_PIN);  // Param 2 - Touch IRQ Pin - interrupt enabled polling

void setup() {
  Serial.begin(115200);
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, CS_PIN);

  ts.begin();
  //ts.begin(SPI1); // use alternate SPI port
  ts.setRotation(2);
//  while (!Serial && (millis() <= 1000));
}

void loop() {

  // tirqTouched() is much faster than touched().  For projects where other SPI chips
  // or other time sensitive tasks are added to loop(), using tirqTouched() can greatly
  // reduce the delay added to loop() when the screen has not been touched.
  if (ts.tirqTouched()) {
    if (ts.touched()) {
      TS_Point p = ts.getPoint();
      Serial.print("Pressure = ");
      Serial.print(p.z);
      Serial.print(", x = ");
      Serial.print(p.x);
      Serial.print(", y = ");
      Serial.print(p.y);
      delay(100);
      Serial.println();
      Serial.println("------------------------------------------------------------------------");

    }
  }
}