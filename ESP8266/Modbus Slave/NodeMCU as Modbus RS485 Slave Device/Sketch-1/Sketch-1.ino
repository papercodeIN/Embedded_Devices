#include <ModbusRTU.h>
#if defined(ESP8266)
 #include <SoftwareSerial.h>
#endif

SoftwareSerial S(D3, D2); // Software serial port for communicating with RS485 to TTL adapter
ModbusRTU mb;

#define REGN 0
#define SLAVE_ID 1

void setup() {
  Serial.begin(9600); // Serial communication for debugging
  S.begin(9600, SWSERIAL_8N1); // Initialize software serial port
  mb.begin(&S, D0); // Initialize ModbusRTU with software serial port and RE/DE pin connected to D0
  
  mb.slave(SLAVE_ID); // Set up as Modbus RTU slave
  mb.addHreg(REGN);   // Add holding register
  
  pinMode(A0, INPUT); // Set A0 pin as input for analog read
}

void loop() {
  // Read analog value from A0 pin
  int sensorValue = analogRead(A0);
  
  // Update holding register with the analog value
  mb.Hreg(REGN, sensorValue);
  
  // Task to handle Modbus communication
  mb.task();
  
  // Yield to allow other tasks to run
  yield();
}
