#include <sMQTTBroker.h>

// Define MQTT client username and password
const char* MQTT_CLIENT_USER = "admin"; // Username for MQTT clients. Set your own value here.
const char* MQTT_CLIENT_PASSWORD = "password"; // Password for MQTT clients. Set your own value here.

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
            };
            break;

            case LostConnect_sMQTTEventType:
                // Handle lost connection event, attempt to reconnect Wi-Fi
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
    Serial.begin(115200);

    // Define static IP address, gateway, subnet mask, and DNS server for the ESP32 in AP mode
    IPAddress local_IP(192, 168, 4, 1);  // Replace with your desired IP address
    IPAddress gateway(192, 168, 4, 1);   // Replace with your desired gateway
    IPAddress subnet(255, 255, 255, 0);  // Replace with your desired subnet mask
    IPAddress primaryDNS(8, 8, 8, 8);    // Optional: replace with your desired primary DNS
    IPAddress secondaryDNS(8, 8, 4, 4);  // Optional: replace with your desired secondary DNS

    // Configure the ESP32 AP with the specified IP details
    if (!WiFi.softAPConfig(local_IP, gateway, subnet)) {
        Serial.println("AP Config failed.");
    }

    // Set up Wi-Fi in Access Point mode
    WiFi.softAP("MQTT_Broker_AP", "12345678");  // Replace with your SSID and password

    // Display the IP address of the ESP32
    Serial.print("AP IP address: ");
    Serial.println(WiFi.softAPIP());

    // Initialize the MQTT broker on port 1883
    const unsigned short mqttPort = 1883;
    broker.init(mqttPort);

    // Additional setup code can be added here
}

void loop() {
    // Update the broker to process incoming and outgoing MQTT messages
    broker.update();

    // Additional loop code can be added here
}