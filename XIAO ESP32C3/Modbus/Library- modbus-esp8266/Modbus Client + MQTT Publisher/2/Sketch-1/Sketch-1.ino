#include <WiFi.h>
#include <ModbusIP_ESP8266.h>
#include <PubSubClient.h>

const char* ssid = "Capgemini_4G";
const char* password = "MN704116";

const char* mqtt_server = "192.168.1.7";
const int mqtt_port = 1883; // Default MQTT port

IPAddress remote(192, 168, 1, 7);  // Address of Modbus Slave device
const int INTERVAL = 1000;         // Interval between reads (in milliseconds)

WiFiClient espClient;
PubSubClient mqttClient(espClient);

ModbusIP mb;

// Define multiple sets of holding register values
const int NUM_SETS = 3;
const int START_REGS[NUM_SETS] = {0, 10, 20};  // Starting holding register addresses for each set
const int NUM_REGS[NUM_SETS] = {5, 5, 5};    // Number of holding registers to read for each set

uint16_t res[NUM_SETS][10];  // Array to hold holding register values for each set
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
      // Read holding registers for each set
      for (int i = 0; i < NUM_SETS; i++) {
        uint8_t retryCount = 0;
        uint8_t transaction;
        
        do {
          transaction = mb.readHreg(remote, START_REGS[i], res[i], NUM_REGS[i], nullptr, 1);
          delay(10); // Small delay before checking transaction status
          mb.task(); // Process Modbus tasks
          retryCount++;
        } while (mb.isTransaction(transaction) && retryCount < 3); // Retry up to 3 times if transaction is active

        if (retryCount >= 3) {
          Serial.println("Failed to read Modbus data after multiple retries");
          // Implement error handling or recovery mechanism here
        }
      }

      // Publish holding register values to MQTT for each set
      for (int i = 0; i < NUM_SETS; i++) {
        for (int j = 0; j < NUM_REGS[i]; j++) {
          char topic[50];
          snprintf(topic, sizeof(topic), "modbus/register/Set%d/HR%d", i, START_REGS[i] + j);
          mqttClient.publish(topic, String(res[i][j]).c_str());
        }
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
