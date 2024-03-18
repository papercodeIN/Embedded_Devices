#include <ModbusRTU.h>
#include <SoftwareSerial.h>
 
SoftwareSerial S(D3, D2); // Software serial port for communicating with RS485 to TTL adapter
ModbusRTU mb;

bool cb(Modbus::ResultCode event, uint16_t transactionId, void* data) { // Callback function to monitor errors
  if (event != Modbus::EX_SUCCESS) {
    Serial.print("Request result: 0x");
    Serial.print(event, HEX);
  }
  return true;
}

void setup() {
  Serial.begin(9600); // Serial communication for debugging
  S.begin(9600, SWSERIAL_8N1); // Initialize software serial port
  mb.begin(&S, D0); // Initialize ModbusRTU with software serial port and RE/DE pin connected to D0
  mb.master(); // Set up as Modbus RTU master
}

uint16_t adc_val;
void loop() {
  if (!mb.slave()) { // Check if not operating as Modbus RTU slave
    adc_val = analogRead(A0); // Read analog voltage from pin A0
    Serial.print("ADC val:");
    Serial.println(adc_val);
    mb.writeHreg(1, 0, adc_val, cb); // Upload analog value to first holding register (address 0)
    
    while (mb.slave()) { // Check if transaction is active
      mb.task();
    }
    delay(10); // Adjust delay as needed
  }
}
