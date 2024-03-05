#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

const char* ssid = "Capgemini_4G";
const char* password = "MN704116";

IPAddress remote(192, 168, 1, 7);  // Address of Modbus Slave device
const int START_COIL = 0;           // Starting coil address
const int NUM_COILS = 10;           // Number of coils to read
const int INTERVAL = 5000;          // Interval between reads (in milliseconds)

WiFiClient client;
ModbusIP mb;

bool res[NUM_COILS];
uint32_t LastModbusRequest = 0;  // Variable to track the last Modbus request time

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize Modbus client
  mb.client();
}

void loop() {
  if (millis() - LastModbusRequest >= INTERVAL) {
    LastModbusRequest = millis();

    if (mb.isConnected(remote)) {  
      // Read coils from Modbus Slave
      uint8_t transaction = mb.readCoil(remote, START_COIL, res, NUM_COILS, nullptr, 1);
      
      // Wait for the transaction to complete
      while(mb.isTransaction(transaction)) {
        mb.task();
        delay(10);
      }

      // Print coil values
      Serial.println("Coil Values:");
      for (int i = 0; i < NUM_COILS; i++) {
        Serial.print("Coil ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(res[i] ? "ON" : "OFF");
      }
    } else {
      // If not connected, try to connect
      mb.connect(remote);
    }
  }
}
