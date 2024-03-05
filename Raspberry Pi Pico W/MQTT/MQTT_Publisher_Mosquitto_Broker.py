import network
from umqtt.simple import MQTTClient
import machine
import time

# ===============================================
# connect to a network
station = network.WLAN(network.STA_IF)
if station.active() and station.isconnected():
    station.disconnect()
    time.sleep(1)
station.active(False)
time.sleep(1)
station.active(True)

# station.connect('SSID', 'PASSWORD')
station.connect('Fusion Automate', 'Fusion_Automate')
time.sleep(1)

while True:
    print('Waiting for WiFi connection...')
    if station.isconnected():
        print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')
        break
    time.sleep(2)
# ===============================================

# Define MQTT Broker credentials
MQTT_BROKER_IP = '192.168.29.221'
MQTT_BROKER_PORT = 1883
MQTT_CLIENT_ID = 'Pico_W_Mqtt_Client'
MQTT_TOPIC = 'Pico_W/Sensor/Internal_Temperature'

# Define MQTT client
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER_IP, MQTT_BROKER_PORT,keepalive=30)
mqtt_client.connect()

# Define function to read sensor value
def read_sensor():
    temperature = 27 - ((machine.ADC(4).read_u16() * (3.3 / (65535))) - 0.706)/0.001721
    return round(temperature,1)

# Publish sensor value to MQTT Broker
while True:
    mqtt_client.publish(MQTT_TOPIC, str(read_sensor()))
    time.sleep(5) # Change the value to adjust publishing frequency

mqtt_client.disconnect()
