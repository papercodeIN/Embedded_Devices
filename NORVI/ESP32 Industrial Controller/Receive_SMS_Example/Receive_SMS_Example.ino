#define GSM_RX 33
#define GSM_TX 32

unsigned long int timer1 = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting GSM SMS Receiver");

  Serial2.begin(9600, SERIAL_8N1, GSM_TX, GSM_RX);

  // Wait for GSM module to initialize
  delay(2000);

  // Test GSM modem with AT command
  sendATCommand("AT", 5000);

  // Check SIM card status
  sendATCommand("AT+CPIN?", 5000);

  // Set GSM module to text mode for SMS
  sendATCommand("AT+CMGF=1", 5000);

  // Configure to show new message indications
  sendATCommand("AT+CNMI=2,2,0,0,0", 5000);

  Serial.println("Ready to receive SMS");
}

void loop() {
  if (Serial2.available()) {
    String incomingData = Serial2.readString(); // Read entire incoming data
    Serial.println("Raw SMS Data:");
    Serial.println(incomingData); // Print raw SMS data

    if (incomingData.indexOf("+CMT:") >= 0) {
      parseSMS(incomingData); // Parse and extract SMS data
    }
  }
}

// Function to send AT commands to GSM module and wait for response
void sendATCommand(const char* command, unsigned long timeout) {
  timer1 = millis();
  Serial2.println(command);  // Send command to GSM module
  Serial.print("Sent command: ");
  Serial.println(command);

  // Wait for response
  while (millis() < timer1 + timeout) {
    while (Serial2.available()) {
      int inByte = Serial2.read();
      Serial.write(inByte);  // Print response from GSM module
    }
  }
  Serial.println();  // Print a newline after the response
}

// Function to parse and extract SMS details
void parseSMS(String rawData) {
  int senderStart = rawData.indexOf("\"") + 1; // Find the first quote
  int senderEnd = rawData.indexOf("\"", senderStart); // Find the closing quote for the sender
  String senderNumber = rawData.substring(senderStart, senderEnd);

  Serial.print("Sender: ");
  Serial.println(senderNumber);

  int messageStart = rawData.indexOf("\n", senderEnd) + 1; // Find the newline after sender
  String messageBody = rawData.substring(messageStart); // Extract the message content

  messageBody.trim(); // Trim extra spaces/newlines in place

  Serial.print("Message: ");
  Serial.println(messageBody); // Print the trimmed message
}

