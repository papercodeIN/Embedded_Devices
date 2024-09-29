import time
from machine import ADC
from umqtt.simple import MQTTClient

# WiFi and MQTT Broker Configuration
WIFI_SSID = ""           # WiFi SSID (Network name)
WIFI_PASSWORD = ""       # WiFi password
MQTT_BROKER = ""         # MQTT Broker address (IP or hostname)
MQTT_PORT = 1883         # MQTT port (default is 1883 for non-secure communication)
MQTT_TOPIC = "Internal Pico-W Temp"  # Topic to publish temperature data

# ADC Configuration
ADCPIN = 4               # ADC pin on Raspberry Pi Pico W for reading internal temperature
adc = ADC(ADCPIN)        # Initialize ADC object for reading analog data

# MQTT Client Configuration
client = MQTTClient("pico_client", MQTT_BROKER, MQTT_PORT)  # Initialize MQTT client with a client ID and broker details

def read_temperature():
    """
    Reads the internal temperature of the Raspberry Pi Pico W using the ADC,
    converts the analog value to a voltage, and then calculates the temperature in Celsius.
    """
    adc_value = adc.read_u16()   # Read the raw ADC value (0-65535)
    volt = (3.3 / 65535) * adc_value  # Convert ADC value to voltage (3.3V max)
    temperature = 27 - (volt - 0.706) / 0.001721  # Convert voltage to temperature in Celsius
    return round(temperature, 1)  # Round temperature to 1 decimal place and return

def connect_to_wifi():
    """
    Connects to the WiFi network using the provided SSID and password.
    """
    import network
    station = network.WLAN(network.STA_IF)  # Set WiFi interface to Station mode
    station.active(True)                    # Activate the interface
    station.connect(WIFI_SSID, WIFI_PASSWORD)  # Connect to WiFi
    while not station.isconnected():        # Wait until connection is established
        pass
    print("Connected to WiFi")  # Print confirmation

def connect_to_mqtt():
    """
    Connects to the MQTT broker.
    """
    client.connect()  # Connect to the MQTT broker
    print("Connected to MQTT Broker")  # Print confirmation

def publish_temperature():
    """
    Publishes the temperature data to the configured MQTT topic.
    """
    temperature = read_temperature()  # Read the current temperature
    client.publish(MQTT_TOPIC, str(temperature))  # Publish the temperature to the MQTT topic
    # print("Published temperature:", temperature)  # Uncomment to print published temperature

def main():
    """
    Main function to connect to WiFi, MQTT, and publish temperature data in a loop.
    """
    connect_to_wifi()  # Connect to WiFi
    connect_to_mqtt()  # Connect to MQTT broker
    while True:        # Infinite loop to continuously publish data
        publish_temperature()  # Publish the temperature
        time.sleep(5)  # Wait for 5 seconds before the next publication

if __name__ == "__main__":
    main()  # Run the main function
