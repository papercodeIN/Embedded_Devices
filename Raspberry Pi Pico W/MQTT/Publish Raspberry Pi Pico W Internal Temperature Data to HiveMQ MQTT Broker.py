import time
import network
import ubinascii
import machine
from umqtt.simple import MQTTClient
import sys

# MQTT Configurations
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = b"pico/w/temperature"

# Wi-Fi Credentials
WIFI_SSID = "Capgemini_4G"
WIFI_PASSWORD = "MN704116"

# Function to connect to Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

# Function to get internal temperature of Raspberry Pi Pico W
def get_internal_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor
    # Calculate temperature in Celsius
    temperature = 27 - (reading - 0.706) / 0.001721
    return temperature

# MQTT Publish function
def publish_temperature(client):
    try:
        temperature = get_internal_temp()
        print(f"Publishing Temperature: {temperature:.2f}°C")
        client.publish(MQTT_TOPIC, b"%.2f" % temperature)
    except Exception as e:
        print(f"Failed to publish temperature: {e}")

# Main function
def main():
    # Connect to Wi-Fi
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)

    # Create MQTT client and connect to broker
    client_id = ubinascii.hexlify(machine.unique_id())
    client = MQTTClient(client_id, MQTT_BROKER, MQTT_PORT)

    try:
        client.connect()
        print("Connected to MQTT Broker")
    except Exception as e:
        print(f"Failed to connect to MQTT Broker: {e}")
        sys.exit()

    # Publish temperature every 10 seconds
    while True:
        publish_temperature(client)
        time.sleep(5)  # Publish every 10 seconds

if __name__ == "__main__":
    main()