#define GSM_RX 33
#define GSM_TX 32

unsigned long int timer1 = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting GSM Call Dialer");

  Serial2.begin(9600, SERIAL_8N1, GSM_TX, GSM_RX);

  // Wait for GSM module to initialize
  delay(2000);

  // Test GSM modem with AT command
  sendATCommand("AT", 5000);  // Test modem communication

  // Check SIM card status
  sendATCommand("AT+CPIN?", 5000);

  // Make a call to a specified number
  makeCall("+91XXXXXXXXXX");  // Replace with the number you want to call

  Serial.println("GSM Call Test Done");
}

void loop() {
  // Nothing to do in loop for now, as we are just making a call once in setup
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

// Function to make a call to a given phone number
void makeCall(const char* phoneNumber) {
  Serial.print("Making call to: ");
  Serial.println(phoneNumber);

  // Send AT command to dial the number
  Serial2.print("ATD");
  Serial2.print(phoneNumber);
  Serial2.println(";");  // Semi-colon is required to initiate the call

  delay(5000);  // Wait a few seconds to let the call go through (optional)

  // After the call is made, you can add code to handle call termination if needed
  // For example, to hang up, you can send the command:
  // sendATCommand("ATH", 5000);  // Hang up the call
}
