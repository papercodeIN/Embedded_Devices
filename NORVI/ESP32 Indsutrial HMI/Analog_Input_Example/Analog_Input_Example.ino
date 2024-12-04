#include <Adafruit_ADS1X15.h>    // Include the Adafruit library for ADS1115 ADC
Adafruit_ADS1115 ads2;           // Create an instance of the ADS1115 object

#include "Wire.h"                // Include the Wire library for I2C communication

#define SDA 19                   // Define the SDA (Serial Data) pin
#define SCL 20                   // Define the SCL (Serial Clock) pin

void setup() {
  Serial.begin(9600);            // Initialize serial communication at 9600 baud rate
  Wire.begin(SDA, SCL);          // Initialize I2C communication with specified SDA and SCL pins
  
  // Initialize the ADS1115 with I2C address 0x49
  if (!ads2.begin(0x49)) {
    Serial.println("Failed to initialize ADS 1.");  // Print error message if initialization fails
  }
  
  ads2.setGain(GAIN_ONE);        // Set the gain to 1x (Full scale ±4.096V)
}

void loop() {
  int adc0 = 0, adc1 = 0, adc2 = 0, adc3 = 0;   // Initialize variables to store ADC readings
  
  // Read the analog values from each of the four channels (AIN0 to AIN3)
  adc0 = ads2.readADC_SingleEnded(0);           // Read from channel 0 (AIN0)
  adc1 = ads2.readADC_SingleEnded(1);           // Read from channel 1 (AIN1)
  adc2 = ads2.readADC_SingleEnded(2);           // Read from channel 2 (AIN2)
  adc3 = ads2.readADC_SingleEnded(3);           // Read from channel 3 (AIN3)
  
  // Print the ADC values to the serial monitor
  Serial.print("AIN1: "); Serial.print(adc0); Serial.println(" ");
  Serial.print("AIN2: "); Serial.print(adc1); Serial.println(" ");
  Serial.print("AIN3: "); Serial.print(adc2); Serial.println(" ");
  Serial.print("AIN4: "); Serial.print(adc3); Serial.println(" ");
  
  // Print a separator line to distinguish between readings
  Serial.println("-----------------------------------------------------------");
  
  delay(500);   // Delay for 500 milliseconds before the next loop iteration
}
