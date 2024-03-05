#include "DHT.h"
#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

#define DHTPIN D6
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Capgemini_4G";
const char* password = "MN704116";

ModbusIP  mb;

void setup() {
  Serial.begin(115200);
  
  // Set fixed IP address, subnet mask, gateway, and DNS server
  IPAddress ip(192, 168, 1, 4);
  IPAddress gateway(192, 168, 1, 1);
  IPAddress subnet(255, 255, 255, 0);
  IPAddress dns(8, 8, 8, 8); // Google DNS

  // Connect to WiFi with fixed IP configuration
  WiFi.begin(ssid, password);
  WiFi.config(ip, gateway, subnet, dns);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  
  // Print assigned IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Initialize DHT sensor
  dht.begin();

  // Initialize Modbus server
  mb.server();
  mb.addCoil(0); // Dummy coil to indicate server running
  mb.addHreg(0); // Register to hold temperature (16-bit integer)
  mb.addHreg(1); // Register to hold humidity (16-bit integer)
}

void loop() {
  // Read temperature and humidity
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  // Update Modbus registers
  mb.Hreg(0, temp * 10); // Temperature (multiplied by 10 to avoid floating point)
  mb.Hreg(1, hum * 10);  // Humidity (multiplied by 10 to avoid floating point)

  // Handle Modbus communication
  mb.task();

  // Print data to serial monitor
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print("*C");
  Serial.print(" Humidity: ");
  Serial.print(hum);
  Serial.println("%");

  delay(500); // Delay before next reading
}
