#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

const char* ssid = "Capgemini_4G";
const char* password = "MN704116";

IPAddress remote(192, 168, 1, 7);  // Address of Modbus Slave device
const int START_INPUT = 0;           // Starting input address
const int NUM_INPUTS = 10;           // Number of inputs to read
const int INTERVAL = 5000;         // Interval between reads (in milliseconds)

WiFiClient client;
ModbusIP mb;

bool res[NUM_INPUTS];
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
      // Read input status from Modbus Slave
      uint8_t transaction = mb.readIsts(remote, START_INPUT, res, NUM_INPUTS, nullptr, 1);
      
      // Wait for the transaction to complete
      while(mb.isTransaction(transaction)) {
        mb.task();
        delay(10);
      }

      // Print input status values
      Serial.println("Input Status Values:");
      for (int i = 0; i < NUM_INPUTS; i++) {
        Serial.print("Input ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(res[i]);
      }
    } else {
      // If not connected, try to connect
      mb.connect(remote);
    }
  }
}
