#define INPUT1 27  // Define a constant INPUT1 and set it to pin 27

void setup() { 
   Serial.begin(9600);  // Initialize serial communication at a baud rate of 9600
   Serial.println("Device Starting");  // Print a message to indicate the device is starting
   pinMode(INPUT1, INPUT);  // Configure pin 27 as an input
} 

void loop() { 
   Serial.print(digitalRead(INPUT1));  // Read the digital state of pin 27 and print it to the serial monitor
   Serial.println("");  // Print a newline character to separate each reading
   delay(500);  // Wait for 500 milliseconds before the next reading
}
