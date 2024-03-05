#include <ModbusMaster.h>  //Library for using ModbusMaster
#define MAX485_DE 3
#define MAX485_RE_NEG 2

ModbusMaster node;  //object node for class ModbusMaster
bool state = true;
bool state1 = false;

void preTransmission()  //Function for setting stste of Pins DE & RE of RS-485
{
  digitalWrite(MAX485_RE_NEG, 1);
  digitalWrite(MAX485_DE, 1);
}

void postTransmission() {
  digitalWrite(MAX485_RE_NEG, 0);
  digitalWrite(MAX485_DE, 0);
}

void setup() {
  pinMode(8, OUTPUT);
  digitalWrite(8, 1);

  pinMode(MAX485_RE_NEG, OUTPUT);
  pinMode(MAX485_DE, OUTPUT);

  digitalWrite(MAX485_RE_NEG, 0);
  digitalWrite(MAX485_DE, 0);
  Serial.begin(9600);                     //Baud Rate as 9600
  node.begin(1, Serial);                  //Slave ID as 1
  node.preTransmission(preTransmission);  //Callback for configuring RS-485 Transreceiver correctly
  node.postTransmission(postTransmission);
}

void loop() {
  uint8_t result;
  uint16_t temperature;
  uint16_t humidity;

  // Clear the serial output window
  Serial.flush();

  // Read the 2nd and 3rd input registers (temperature and humidity)
  result = node.readInputRegisters(0x0001, 2);  // Read 2 input registers starting from address 40002
  if (result == node.ku8MBSuccess) {
    temperature = node.getResponseBuffer(0) / 10;  // Divide by 10 to get actual value
    humidity = node.getResponseBuffer(1) / 10;     // Divide by 10 to get actual value

    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  } else {
    Serial.println("Read error");
  }

  delay(1000);
}