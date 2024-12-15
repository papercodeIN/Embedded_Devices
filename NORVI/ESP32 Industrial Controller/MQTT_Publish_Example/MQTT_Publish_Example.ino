#include <SoftwareSerial.h>
#include <PubSubClient.h>

#define GSM_RX 33
#define GSM_TX 32
#define SerialMon Serial  // Use Serial for debugging

// MQTT Broker details
const char* mqttServer = "your.mqtt.server";  // Replace with your broker's IP or domain
const int mqttPort = 1883;                    // Usually 1883 for MQTT, or 8883 for MQTT over SSL
const char* mqttUser = "your_mqtt_username";  // MQTT username
const char* mqttPassword = "your_mqtt_password";  // MQTT password
const char* mqttTopic = "your/mqtt/topic";    // Topic to publish

// Create an instance of the SoftwareSerial and PubSubClient
SoftwareSerial gsmSerial(GSM_RX, GSM_TX);  // RX, TX pins for GSM module
PubSubClient client(gsmSerial);

// GSM settings
const char* apn = "your_apn";  // APN from your mobile carrier
const char* gprsUser = "";     // GPRS username (if required)
const char* gprsPassword = ""; // GPRS password (if required)

void setup() {
  // Start serial communication for debugging
  SerialMon.begin(115200);
  gsmSerial.begin(9600); // Start communication with GSM module

  // Initialize GSM module
  SerialMon.println("Initializing GSM Module...");
  initializeGSM();

  // Set MQTT server
  client.setServer(mqttServer, mqttPort);

  // Connect to the MQTT server
  if (connectToMQTT()) {
    SerialMon.println("Connected to MQTT Broker");
  } else {
    SerialMon.println("Failed to connect to MQTT Broker");
  }

  // Publish a message
  publishMQTTMessage("Hello from GSM Module!");

  // Loop to keep sending messages periodically
  while (true) {
    if (!client.connected()) {
      reconnectMQTT();
    }
    client.loop(); // Keep the MQTT connection alive
    delay(10000); // Wait for 10 seconds before sending the next message
  }
}

void initializeGSM() {
  // Send AT command to initialize GSM module and check if it's ready
  sendATCommand("AT", 5000);
  sendATCommand("AT+CSQ", 5000);  // Check signal quality
  sendATCommand("AT+CGATT?", 5000);  // Check GPRS attach status

  // Set the APN for your mobile carrier
  String apnCommand = "AT+CGDCONT=1,\"IP\",\"" + String(apn) + "\"";
  sendATCommand(apnCommand.c_str(), 5000);

  // Enable GPRS
  sendATCommand("AT+CGACT=1,1", 5000);  // Activate GPRS

  // Wait for a while to ensure the connection is established
  delay(5000);
}

void sendATCommand(const char* command, unsigned long timeout) {
  gsmSerial.println(command);
  unsigned long startTime = millis();
  while (millis() - startTime < timeout) {
    if (gsmSerial.available()) {
      char c = gsmSerial.read();
      SerialMon.write(c);  // Print response from GSM module
    }
  }
  SerialMon.println();
}

bool connectToMQTT() {
  // Attempt to connect to MQTT broker
  while (!client.connected()) {
    SerialMon.print("Connecting to MQTT...");
    if (client.connect("GSMClient", mqttUser, mqttPassword)) {
      SerialMon.println("Connected");
    } else {
      SerialMon.print("Failed, rc=");
      SerialMon.print(client.state());
      delay(5000);
    }
  }
  return client.connected();
}

void reconnectMQTT() {
  // Reconnect to the MQTT broker if disconnected
  while (!client.connected()) {
    SerialMon.print("Reconnecting to MQTT...");
    if (client.connect("GSMClient", mqttUser, mqttPassword)) {
      SerialMon.println("Reconnected");
    } else {
      SerialMon.print("Failed, rc=");
      SerialMon.print(client.state());
      delay(5000);
    }
  }
}

void publishMQTTMessage(const char* message) {
  if (client.connected()) {
    client.publish(mqttTopic, message);
    SerialMon.println("Message Published: " + String(message));
  } else {
    SerialMon.println("MQTT not connected");
  }
}

void loop() {
  // Nothing to do here, as the main loop handles MQTT communication
}
