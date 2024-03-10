#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

const char* ssid = "Capgemini_4G";
const char* password = "MN704116";

ModbusIP mb;

void setup() {
  Serial.begin(115200);

  // Set fixed IP address, subnet mask, and gateway
  IPAddress ip(192, 168, 1, 5);
  IPAddress subnet(255, 255, 255, 0);
  IPAddress gateway(192, 168, 1, 1);

  // Connect to WiFi with fixed IP configuration
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  // Print assigned IP address
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Initialize Modbus server
  mb.server(4444);
  
  // Add 20 holding registers
  for (int i = 0; i < 20; i++) {
    mb.addHreg(i, 0); // Initialize all holding registers to zero
  }
}

void loop() {
  // Handle Modbus communication
  mb.task();
  delay(100); // Adjust delay as needed depending on your application requirements
}
