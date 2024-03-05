import time
from machine import ADC
from umqtt.simple import MQTTClient

# WiFi and MQTT Broker Configuration
WIFI_SSID = ""
WIFI_PASSWORD = ""
MQTT_BROKER = ""
MQTT_PORT = 1883
MQTT_TOPIC = "Internal Pico-W Temp"

# ADC Configuration
ADCPIN = 4
adc = ADC(ADCPIN)

# MQTT Client Configuration
client = MQTTClient("pico_client", MQTT_BROKER, MQTT_PORT)

def read_temperature():
    adc_value = adc.read_u16()
    volt = (3.3 / 65535) * adc_value
    temperature = 27 - (volt - 0.706) / 0.001721
    return round(temperature, 1)

def connect_to_wifi():
    import network
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(WIFI_SSID, WIFI_PASSWORD)
    while not station.isconnected():
        pass
    print("Connected to WiFi")

def connect_to_mqtt():
    client.connect()
    print("Connected to MQTT Broker")

def publish_temperature():
    temperature = read_temperature()
    client.publish(MQTT_TOPIC, str(temperature))
    #print("Published temperature:", temperature)

def main():
    connect_to_wifi()
    connect_to_mqtt()
    while True:
        publish_temperature()
        time.sleep(5)  # Publish temperature every 5 seconds

if __name__ == "__main__":
    main()
