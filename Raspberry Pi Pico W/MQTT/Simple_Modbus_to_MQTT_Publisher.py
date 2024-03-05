import network
from umqtt.simple import MQTTClient
from umodbus.tcp import TCP as ModbusTCPMaster
import time

# Define MQTT broker details
MQTT_BROKER = '192.168.29.221'
MQTT_PORT = 1883


# Define Modbus TCP Client details
MODBUS_TCP_IP = '192.168.29.221'
MODBUS_TCP_PORT = 502

# Define MQTT topics
MQTT_PUBLISH_TOPIC = 'Pico_W/Modbus/HR'

# Define Modbus device details
MODBUS_DEVICE_ID = 1
MODBUS_READ_REGISTER_ADDRESS = 0
MODBUS_READ_REGISTER_COUNT = 10

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


# Create MQTT client instance and set callback function
mqtt_client = MQTTClient(client_id='{MQTT_client_id}', server=MQTT_BROKER, port=MQTT_PORT, keepalive=30)
mqtt_client.connect()

modbus_client = ModbusTCPMaster(slave_ip=MODBUS_TCP_IP,slave_port=MODBUS_TCP_PORT,timeout=5)

# Loop to read Modbus registers and publish to MQTT broker
while True:
    # Read Modbus registers
    modbus_values = modbus_values = modbus_client.read_holding_registers(slave_addr=MODBUS_DEVICE_ID,starting_addr=MODBUS_READ_REGISTER_ADDRESS,register_qty=MODBUS_READ_REGISTER_COUNT)
    print(modbus_values)
    if modbus_values:
        # Publish Modbus register values to MQTT broker
        mqtt_client.publish(MQTT_PUBLISH_TOPIC, str(modbus_values))
    else:
        print("Error Reading Modbus Values.")
    mqtt_client.check_msg()
    time.sleep(1)

