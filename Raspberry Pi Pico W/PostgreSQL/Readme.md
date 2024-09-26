# Project Description: Raspberry Pi Pico W Temperature Logger

This project utilizes a **Raspberry Pi Pico W** to continuously monitor and log internal temperature readings into a **PostgreSQL database** over a Wi-Fi connection. The setup involves the following key components and functionalities:

## Key Features

1. **Wi-Fi Connectivity**: 
   - The Raspberry Pi Pico W connects to a specified Wi-Fi network using the provided SSID and password, allowing it to communicate with remote servers.

2. **PostgreSQL Database Connection**: 
   - The device establishes a connection to a PostgreSQL database hosted on a remote server, handling any connection errors gracefully while providing feedback on the connection status.

3. **Temperature Reading**: 
   - The internal temperature of the Raspberry Pi Pico W is read using the on-board ADC (Analog-to-Digital Converter). The raw ADC value is converted into a Celsius temperature value using a simple calibration formula.

4. **Data Logging**: 
   - Temperature readings are inserted into a database table named `sensor_data` every 10 seconds. The system checks for any errors during data insertion and reports them.

5. **Continuous Monitoring**: 
   - The program runs in an infinite loop, continuously reading the temperature and logging the data until manually interrupted by the user.

## Compatibility with Other Microcontrollers

This project can also be adapted to work with **ESP32** and **ESP8266** microcontrollers:

- **Wi-Fi Connectivity**: Both the ESP32 and ESP8266 have built-in Wi-Fi capabilities, allowing for similar Wi-Fi connections.
- **Database Connection**: The `micropg_lite` library is compatible with ESP32 and ESP8266, allowing for PostgreSQL database connections.
- **Temperature Reading**: The ESP32 can use its internal sensor, while the ESP8266 can interface with external temperature sensors (e.g., DHT11, DS18B20).

## Conclusion

This project serves as a practical example of **IoT (Internet of Things)** data logging, showcasing how microcontrollers can be integrated with cloud-based databases for real-time data monitoring and analysis. It can be further expanded with features such as data visualization, alerting systems, or additional sensors for comprehensive environmental monitoring.

## Create Table Query if Table do not Exists
```
CREATE TABLE IF NOT EXISTS sensor_data ( id SERIAL PRIMARY KEY, temperature FLOAT NOT NULL, recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )
```
