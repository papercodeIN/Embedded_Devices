#include <sMQTTBroker.h>

// Define MQTT client username and password
const char* MQTT_CLIENT_USER = "admin"; // Username for MQTT clients
const char* MQTT_CLIENT_PASSWORD = "password"; // Password for MQTT clients

// Create a custom class inheriting from sMQTTBroker
class MyBroker : public sMQTTBroker {
public:
    // Override the onEvent function to handle different MQTT events
    bool onEvent(sMQTTEvent *event) override {
        switch(event->Type()) {
            case NewClient_sMQTTEventType: {
                // Handle new client connection event
                sMQTTNewClientEvent *e = (sMQTTNewClientEvent*)event;

                // Check if the provided username and password are correct
                if ((e->Login() != MQTT_CLIENT_USER) || (e->Password() != MQTT_CLIENT_PASSWORD)) {
                    Serial.println("Invalid username or password");
                    return false; // Deny connection if credentials are incorrect
                }
            }
            break;

            case LostConnect_sMQTTEventType:
                // Handle lost connection event; attempt to reconnect Wi-Fi
                WiFi.reconnect();
                break;

            case UnSubscribe_sMQTTEventType:
            case Subscribe_sMQTTEventType: {
                // Handle subscribe/unsubscribe events
                sMQTTSubUnSubClientEvent *e = (sMQTTSubUnSubClientEvent*)event;
                // You can add additional code here to handle these events if needed
            }
            break;
        }
        return true; // Return true to allow the event to be processed normally
    }
};

// Instantiate the broker object
MyBroker broker;

void setup() {
    Serial.begin(115200); // Initialize serial communication at 115200 baud

    // Connect to Wi-Fi network
    const char *ssid = "WIIF_SSID";      // Replace with your Wi-Fi SSID
    const char *password = "WIFI_PASSWORD"; // Replace with your Wi-Fi password
    WiFi.begin(ssid, password); // Start Wi-Fi connection

    // Wait until the ESP32 is connected to Wi-Fi
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000); // Delay for 1 second
    }

    // Connection established
    Serial.println("Connection established!");
    Serial.print("IP address:\t");
    Serial.println(WiFi.localIP()); // Print the IP address assigned to the ESP32

    // Initialize the MQTT broker on port 1883
    const unsigned short mqttPort = 1883;
    broker.init(mqttPort);
}

void loop() {
    // Update the broker to process incoming and outgoing MQTT messages
    broker.update();
}