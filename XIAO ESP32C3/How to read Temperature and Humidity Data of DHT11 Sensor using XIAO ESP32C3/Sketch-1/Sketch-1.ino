#include "DHT.h"

#define DHTPIN D6
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

float temp;  //to store the temperature value
float hum;   // to store the humidity value

void setup() {
  Serial.begin(115200);
  dht.begin();  //Begins to receive Temperature and humidity values.
}

void loop() {
  // ping adafruit io a few times to make sure we remain connected
  temp = dht.readTemperature();

  hum = dht.readHumidity();
  Serial.print("temperature = ");
  Serial.print(temp);
  Serial.print(" humidity = ");
  Serial.println(hum);

  delay(5000);
}