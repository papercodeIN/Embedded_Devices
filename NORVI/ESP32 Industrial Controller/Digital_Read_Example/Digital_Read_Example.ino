#define INPUT1 27  // Define a constant INPUT1 and set it to pin 27

// #define INPUT2 34
// #define INPUT3 35
// #define INPUT4 14
// #define INPUT5 13
// #define INPUT6 21

void setup() { 
   Serial.begin(9600);  // Initialize serial communication at a baud rate of 9600
   Serial.println("Device Starting");  // Print a message to indicate the device is starting
   pinMode(INPUT1, INPUT);  // Configure pin 27 as an input
} 

void loop() { 
   int inputState = digitalRead(INPUT1);  // Read the digital state of pin 27
   
   if (inputState == HIGH) {  // Check if the input is high
       Serial.println("1");  // Print "1" for high state
   } else { 
       Serial.println("0");  // Print "0" for low state
   }
   
   delay(500);  // Wait for 500 milliseconds before the next reading
}
