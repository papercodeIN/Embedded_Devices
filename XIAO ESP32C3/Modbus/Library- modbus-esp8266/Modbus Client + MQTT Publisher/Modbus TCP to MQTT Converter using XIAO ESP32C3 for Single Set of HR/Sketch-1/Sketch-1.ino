#include <WiFi.h>
#include <ModbusIP_ESP8266.h>
#include <PubSubClient.h>

const char* ssid = "Capgemini_4G";
const char* password = "MN704116";

const char* mqtt_server = "192.168.1.7";
const int mqtt_port = 1883; // Default MQTT port

IPAddress remote(192, 168, 1, 7);  // Address of Modbus Slave device
const int START_REG = 0;           // Starting holding register
const int NUM_REGS = 10;           // Number of holding registers to read
const int INTERVAL = 500;         // Interval between reads (in milliseconds)

WiFiClient espClient;
PubSubClient mqttClient(espClient);

ModbusIP mb;

uint16_t res[NUM_REGS];
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

  // Set up MQTT
  mqttClient.setServer(mqtt_server, mqtt_port);

  // Initialize Modbus client
  mb.client();
}

void loop() {
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }

  mqttClient.loop();

  if (millis() - LastModbusRequest >= INTERVAL) {
    LastModbusRequest = millis();

    if (mb.isConnected(remote)) {  
      // Read holding registers from Modbus Slave
      uint8_t transaction = mb.readHreg(remote, START_REG, res, NUM_REGS, nullptr, 1);
      
      // Wait for the transaction to complete
      while(mb.isTransaction(transaction)) {
        mb.task();
        delay(10);
      }

      // Print holding register values
      // Serial.println("Holding Register Values:");
      // for (int i = 0; i < NUM_REGS; i++) {
      //   Serial.print("Register ");
      //   Serial.print(START_REG + i);
      //   Serial.print(": ");
      //   Serial.println(res[i]);
      // }

      // Publish holding register values to MQTT
      for (int i = 0; i < NUM_REGS; i++) {
        char topic[50];
        snprintf(topic, sizeof(topic), "modbus/register/HR%d", START_REG + i);
        mqttClient.publish(topic, String(res[i]).c_str());
      }
    } else {
      // If not connected, try to connect
      mb.connect(remote);
    }
  }
}

void reconnectMQTT() {
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqttClient.connect("XIAO ESP32C3 Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
