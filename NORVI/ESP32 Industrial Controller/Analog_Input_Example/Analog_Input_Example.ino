#include <Adafruit_ADS1X15.h> 
#include <Wire.h> 

// Create ADS1115 instances for two devices
Adafruit_ADS1115 ads1;  // First ADS1115 device at address 0x48
Adafruit_ADS1115 ads2;  // Second ADS1115 device at address 0x49

void setup() { 
   Serial.begin(9600); 
   Serial.println("Device Starting"); 

   // Initialize I2C communication with custom SDA and SCL pins (16 and 17)
   Wire.begin(16, 17); 

   // Start ADS1115 devices with their respective I2C addresses
   ads1.begin(0x48);  // Initialize ADS1115 at address 0x48
   ads2.begin(0x49);  // Initialize ADS1115 at address 0x49

   // Set gain for both ADS1115 devices to GAIN_ONE (±4.096V range)
   ads1.setGain(GAIN_ONE); 
   ads2.setGain(GAIN_ONE); 
}

void loop() { 
  // Read raw ADC value from channel 0 of the first ADS1115
  int16_t rawValue = ads1.readADC_SingleEnded(0); 
  
  // Convert the raw ADC value to a voltage (0-3.3V range assumed)
  float voltage = mapToVoltage(rawValue); 
  
  // Print the raw value and corresponding voltage
  Serial.print("Analog 0: Raw Value = ");
  Serial.print(rawValue);
  Serial.print(", Mapped Voltage = ");
  Serial.print(voltage, 2);  // Print voltage with 2 decimal places
  Serial.println(" V");
  
  delay(500);  // Delay for readability, adjust as needed
}

// Function to map raw ADC reading to voltage
float mapToVoltage(int16_t adcValue) {
  // ADS1115 provides 16-bit resolution:
  // - In single-ended mode, output range is 0 to 32767 for positive voltages.
  // - With GAIN_ONE (±4.096V), the full-scale value is 32767.
  // - Assuming we map the input range to 0-3.3V.
  return (adcValue * 3.3) / 8240.0;  // Adjust the divisor based on gain and input range
}
