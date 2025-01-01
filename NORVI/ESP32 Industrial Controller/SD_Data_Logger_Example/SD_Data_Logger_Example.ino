#include <SPI.h>
#include <Wire.h>
#include "FS.h"
#include "SD.h"
#include "RTClib.h"

// Pin definition for the SD card chip select (CS) pin
#define SD_CS 15

// Create an RTC_DS3231 object to interface with the RTC module
RTC_DS3231 rtc;

// Array of day names for displaying the day of the week
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

// Global variable to store the current file name
String currentFileName;

// ================================================ SETUP ================================================
void setup() {
  // Initialize the Serial Monitor for debugging
  Serial.begin(115200);
  Serial.println("System Initialized");

  // Initialize the I2C communication for the RTC module (using pins 16 for SDA and 17 for SCL)
  Wire.begin(16, 17);

  // Initialize the SD card interface
  pinMode(SD_CS, OUTPUT);
  digitalWrite(SD_CS, HIGH);  // Set SD card chip select pin high to ensure it's inactive

  // Check if the SD card is initialized correctly
  if (!SD.begin(SD_CS)) {
    // If no SD card is found, print an error message and exit
    Serial.println("No SD card detected");
    return;
  }

  // Check the RTC to make sure it's functioning and set up correctly
  RTC_Check();
  delay(1000);

  // Generate the file name based on the current date
  updateFileName();

  // If the file doesn't exist yet, create it and write headers
  File dataFile = SD.open(currentFileName.c_str(), FILE_WRITE);
  if (dataFile) {
    // Write CSV header with column names: Timestamp and Random Value
    dataFile.println("Timestamp,Random Value");
    dataFile.close();  // Close the file after writing
  }
}

// ================================================ LOOP ================================================
void loop() {
  // Generate a random integer value between 0 and 1023
  int randomValue = random(0, 1024);

  // Log the random value along with a timestamp to the SD card
  logData(randomValue);

  // Delay of 5000ms (5 seconds) before the next loop iteration
  delay(5000);
}

// Function to log data to the SD card with a timestamp
void logData(int randomValue) {
  // Open the CSV file for appending (write to the end of the file)
  File dataFile = SD.open(currentFileName.c_str(), FILE_APPEND);

  if (dataFile) {
    // Get the current date and time from the RTC
    DateTime now = rtc.now();

    // Format the timestamp as "YYYY/MM/DD Weekday HH:MM:SS"
    String timestamp = String(now.year()) + "/" + 
                       String(now.month()) + "/" + 
                       String(now.day()) + " " + 
                       String(daysOfTheWeek[now.dayOfTheWeek()]) + " " + 
                       String(now.hour()) + ":" + 
                       String(now.minute()) + ":" + 
                       String(now.second());

    // Write the timestamp and random value in CSV format
    dataFile.print(timestamp);
    dataFile.print(",");
    dataFile.println(randomValue);

    // Close the file after writing the data
    dataFile.close();

    // Print the logged data to the Serial Monitor for debugging
    Serial.print("Timestamp: ");
    Serial.print(timestamp);
    Serial.print(" - Random Data: ");
    Serial.println(randomValue);
  } else {
    // If there was an error opening the file, print an error message
    Serial.println("Error opening file: " + currentFileName);
  }
}

// Function to check the RTC status and set the time if necessary
void RTC_Check() {
  // Initialize the RTC module
  if (! rtc.begin()) {
    // If the RTC is not found, print an error message
    Serial.println("Couldn't find RTC");
  } else {
    // If the RTC has lost power, adjust the time to the compile-time of the sketch
    if (rtc.lostPower()) {
      Serial.println("RTC lost power, lets set the time!");
      // Adjust the RTC time to the time the sketch was compiled
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));  
    }
  }
}

// Function to generate the file name based on the current date
void updateFileName() {
  // Get the current date from the RTC
  DateTime now = rtc.now();

  // Format the file name as "YYYY-MM-DD.csv"
  currentFileName = "/" + String(now.year()) + "-" + 
                    String(now.month()) + "-" + 
                    String(now.day()) + ".csv";

  // Print the generated file name to the Serial Monitor for debugging
  Serial.println("Generated file name: " + currentFileName);
}
