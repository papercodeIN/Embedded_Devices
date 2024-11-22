#include <ModbusMaster.h>  // Include ModbusMaster library for Modbus communication

// Pin definitions
#define FC 22        // Flow control pin connected to DE/RE of MAX485
#define RX_PIN 25    // Serial receive pin
#define TX_PIN 26    // Serial transmit pin

ModbusMaster node;   // Create ModbusMaster object for handling communication

// Pre-transmission callback: Set DE (Driver Enable) high to enable transmission
void preTransmission() {
  digitalWrite(FC, HIGH);
}

// Post-transmission callback: Set DE low to enable reception
void postTransmission() {
  digitalWrite(FC, LOW);
}

void setup() {
  // Initialize the serial monitor for debugging
  Serial.begin(9600);
  Serial.println("Initializing Modbus Communication...");

  // Configure the flow control pin
  pinMode(FC, OUTPUT);
  digitalWrite(FC, LOW);  // Start in receiving mode

  // Initialize Modbus communication using Serial1
  Serial1.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);

  // Set up Modbus node with slave ID 1
  node.begin(1, Serial1);  // Slave ID: 1
  node.preTransmission(preTransmission);  // Register callback before sending data
  node.postTransmission(postTransmission); // Register callback after sending data
}

void loop() {
  uint8_t result;           // Variable to store the result of the Modbus read operation
  uint16_t temperature;     // Variable to store the temperature value
  uint16_t humidity;        // Variable to store the humidity value

  // Clear the serial buffer to avoid overlapping data
  Serial.flush();

  // Read 2 input registers starting from address 0x0001 (typically 30001 in Modbus terminology)
  result = node.readInputRegisters(0x0001, 2);

  // Check if the read operation was successful
  if (result == node.ku8MBSuccess) {
    // Convert raw Modbus values to temperature and humidity
    // Assumes that the sensor sends data with one decimal place, hence the division by 10
    temperature = node.getResponseBuffer(0) / 10.0;
    humidity = node.getResponseBuffer(1) / 10.0;

    // Display the temperature value
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");

    // Display the humidity value
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  } else {
    // Handle communication failure
    Serial.println("Read error: Unable to retrieve data from Modbus device");
  }

  // Delay for 1 second before reading the next data
  delay(1000);
}
