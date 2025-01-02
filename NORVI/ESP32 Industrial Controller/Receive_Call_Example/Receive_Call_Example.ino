#define GSM_RX 33
#define GSM_TX 32

void setup() {
  Serial.begin(115200);
  Serial.println("Starting GSM Call Receiver");

  Serial2.begin(9600, SERIAL_8N1, GSM_TX, GSM_RX);

  // Wait for GSM module to initialize
  delay(2000);

  // Test GSM modem with AT command
  sendATCommand("AT", 5000);

  // Check SIM card status
  sendATCommand("AT+CPIN?", 5000);

  // Enable Caller ID notification
  sendATCommand("AT+CLIP=1", 5000);

  Serial.println("Ready to receive calls");
}

void loop() {
  if (Serial2.available()) {
    String incomingData = Serial2.readString(); // Read incoming data
    Serial.println("Raw Call Data:");
    Serial.println(incomingData); // Print raw call data

    if (incomingData.indexOf("RING") >= 0 || incomingData.indexOf("+CLIP:") >= 0) {
      parseCallerData(incomingData); // Parse and extract caller data
    }
  }
}

// Function to send AT commands to GSM module and wait for response
void sendATCommand(const char* command, unsigned long timeout) {
  unsigned long start = millis();
  Serial2.println(command);  // Send command to GSM module
  Serial.print("Sent command: ");
  Serial.println(command);

  // Wait for response
  while (millis() - start < timeout) {
    while (Serial2.available()) {
      char c = Serial2.read();
      Serial.write(c);  // Print response from GSM module
    }
  }
  Serial.println();  // Print a newline after the response
}

// Function to parse and extract caller details
void parseCallerData(String rawData) {
  if (rawData.indexOf("+CLIP:") >= 0) {
    int numberStart = rawData.indexOf("\"") + 1; // Find the first quote
    int numberEnd = rawData.indexOf("\"", numberStart); // Find the closing quote
    String callerNumber = rawData.substring(numberStart, numberEnd);

    Serial.print("Incoming call from: ");
    Serial.println(callerNumber);

    // Optionally, you can auto-reject or pick up the call using AT commands
    // Uncomment the following lines to pick up or reject the call:

    // Pick up the call:
    // sendATCommand("ATA", 5000);

    // Reject the call:
    // sendATCommand("ATH", 5000);
  }
}
