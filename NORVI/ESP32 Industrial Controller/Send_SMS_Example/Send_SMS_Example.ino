#define GSM_RX 33
#define GSM_TX 32

unsigned long int timer1 = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting GSM SMS Sender");

  Serial2.begin(9600, SERIAL_8N1, GSM_TX, GSM_RX); 

  // Wait for GSM module to initialize
  delay(2000);

  // Test GSM modem with AT command
  sendATCommand("AT", 5000);  // Test modem communication

  // Check SIM card status
  sendATCommand("AT+CPIN?", 5000);

  // Set GSM module to text mode for SMS
  sendATCommand("AT+CMGF=1", 5000);

  // Send SMS
  sendSMS("+91XXXXXXXXXX", "hello from NORVI GSM Controller");

  Serial.println("GSM SMS Test Done");
}

void loop() {
  // Nothing to do in loop for now, as we are just sending a message once in setup
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

// Function to send SMS to a given phone number with a message
void sendSMS(const char* phoneNumber, const char* message) {
  Serial.print("Sending SMS to: ");
  Serial.println(phoneNumber);

  // Set the recipient's phone number
  Serial2.print("AT+CMGS=\"");
  Serial2.print(phoneNumber);
  Serial2.println("\"");
  delay(1000);

  // Send the message text
  Serial2.println(message);
  delay(1000);

  // Send Ctrl+Z to indicate the end of the message (necessary to send SMS)
  Serial2.write(26);  // ASCII code for Ctrl+Z
  delay(1000);

  // Print out the confirmation
  Serial.println("SMS sent successfully");
}
