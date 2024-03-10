#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

#define DIGITAL_REGISTER_ADDRESS 10

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

  mb.server(8300);
  mb.addCoil(DIGITAL_REGISTER_ADDRESS, false); // Initialize the coil with false (off)
  
  pinMode(D10, OUTPUT); // Set LED_BUILTIN pin as output
}

void loop() {
  mb.task();

  // Read the value from Modbus register to control the LED
  bool ledStatus = mb.Coil(DIGITAL_REGISTER_ADDRESS);

  // Control the LED based on inverted Modbus register value
  digitalWrite(D10, ledStatus ? HIGH : LOW);

  delay(500);
}
