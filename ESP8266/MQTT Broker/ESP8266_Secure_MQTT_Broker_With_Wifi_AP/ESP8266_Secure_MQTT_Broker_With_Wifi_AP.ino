#include <ESP8266WiFi.h>
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>
#include <DHT.h>

#define DHTPIN D4          // Pin where the data line of DHT sensor is connected
#define DHTTYPE DHT11      // DHT11 or DHT22 sensor

DHT dht(DHTPIN, DHTTYPE);

char ssid[] = "your-ssid";         // your WiFi SSID
char pass[] = "your-password";     // your WiFi password

WiFiClient client;                 // WiFi client for the MySQL connection
MySQL_Connection conn(&client);
MySQL_Cursor* cursor;

// MySQL server login credentials and database info
char user[] = "root";              // MySQL username
char password[] = "secret";        // MySQL password
char INSERT_SQL[] = "INSERT INTO test_arduino.hello_sensor (message, sensor_num, value, humidity) VALUES ('Sensor Data', %d, %s, %s)";
char query[128];
char temperature[10];
char humidity[10];

void setup() {
  Serial.begin(115200);
  dht.begin();                     // Initialize DHT sensor

  // Begin WiFi connection
  Serial.printf("Connecting to %s", ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
  Serial.print("My IP address is: ");
  Serial.println(WiFi.localIP());

  // Connect to MySQL server
  Serial.print("Connecting to SQL... ");
  if (conn.connect("your-server-address", 3306, user, password)) {
    Serial.println("Connected to MySQL.");
  } else {
    Serial.println("MySQL connection failed.");
  }
}

void loop() {
  float t = dht.readTemperature();  // Reading temperature
  float h = dht.readHumidity();     // Reading humidity

  // Check if readings are valid
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Convert readings to string format for SQL query
  dtostrf(t, 1, 2, temperature);
  dtostrf(h, 1, 2, humidity);
  sprintf(query, INSERT_SQL, 1, temperature, humidity);  // 1 is a placeholder for sensor number

  // Insert data into MySQL
  if (conn.connected()) {
    MySQL_Cursor *cur_mem = new MySQL_Cursor(&conn);
    cur_mem->execute(query);
    delete cur_mem;  // Clean up
    Serial.println("Data recorded.");
  } else {
    Serial.println("Failed to connect to MySQL.");
  }

  delay(5000);  // Wait for 5 seconds before reading data again
}
