#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

#define ANALOG_REGISTER_ADDRESS 0

ModbusIP mb;

void setup() {
  Serial.begin(115200);
  WiFi.begin("Capgemini_4G", "MN704116");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  mb.server();
  mb.addHreg(ANALOG_REGISTER_ADDRESS, 0);
}

void loop() {
  mb.task();

  int sensorValue = analogRead(A0);
  int mappedValue = map(sensorValue, 0, 4095, 0, 100); // Map sensorValue from 0 to 4095 to 0 to 100
  
  // mb.Hreg(ANALOG_REGISTER_ADDRESS, sensorValue);
  mb.Hreg(ANALOG_REGISTER_ADDRESS, mappedValue);

  // Serial.print("Analog Value: ");
  // Serial.println(mappedValue);

  delay(500);
}
