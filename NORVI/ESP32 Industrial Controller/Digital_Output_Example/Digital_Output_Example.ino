#define OUTPUT1 12
#define OUTPUT2 2

unsigned long timer1 = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("Digital Output Test - Debug Mode");

  // Configure digital outputs
  pinMode(OUTPUT1, OUTPUT);
  pinMode(OUTPUT2, OUTPUT);

  // Initialize outputs to LOW
  digitalWrite(OUTPUT1, LOW);
  digitalWrite(OUTPUT2, LOW);
  Serial.println("Outputs initialized to LOW.");
}

void loop() {
  Serial.println("Starting output sequence...");

  // Turn OUTPUT1 ON and OUTPUT2 OFF
  digitalWrite(OUTPUT1, HIGH);
  digitalWrite(OUTPUT2, LOW);
  Serial.println("OUTPUT1: HIGH, OUTPUT2: LOW");
  delay(5000);

  // Turn OUTPUT1 OFF and OUTPUT2 ON
  digitalWrite(OUTPUT1, LOW);
  digitalWrite(OUTPUT2, HIGH);
  Serial.println("OUTPUT1: LOW, OUTPUT2: HIGH");
  delay(5000);

  // Turn both outputs OFF
  digitalWrite(OUTPUT1, LOW);
  digitalWrite(OUTPUT2, LOW);
  Serial.println("OUTPUT1: LOW, OUTPUT2: LOW");
  delay(5000);

  Serial.println("Output sequence complete. Restarting...");
}
