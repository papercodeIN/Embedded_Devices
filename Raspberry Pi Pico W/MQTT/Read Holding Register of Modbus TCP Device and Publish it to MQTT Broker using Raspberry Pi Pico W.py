import network
from umqtt.simple import MQTTClient
from umodbus.tcp import TCP as ModbusTCPMaster
import time

# Define constants
MQTT_BROKER = '192.168.1.5'
MQTT_PORT = 1883
MODBUS_TCP_IP = '192.168.1.5'
MODBUS_TCP_PORT = 502
MQTT_PUBLISH_TOPIC = 'Pico_W/Modbus/HR'
MODBUS_DEVICE_ID = 1
MODBUS_READ_REGISTER_ADDRESS = 0
MODBUS_READ_REGISTER_COUNT = 10
WIFI_SSID = 'Capgemini_4G'
WIFI_PASSWORD = 'MN704116'

def connect_to_wifi():
    station = network.WLAN(network.STA_IF)
    if station.active() and station.isconnected():
        station.disconnect()
        time.sleep(1)
    station.active(False)
    time.sleep(1)
    station.active(True)
    station.connect(WIFI_SSID, WIFI_PASSWORD)
    while not station.isconnected():
        print('Connecting to WiFi...')
        time.sleep(2)
    print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')
    return station

def connect_to_mqtt():
    mqtt_client = MQTTClient(client_id='{MQTT_client_id}', server=MQTT_BROKER, port=MQTT_PORT, keepalive=30)
    try:
        mqtt_client.connect()
        print('Connected to MQTT broker')
        return mqtt_client
    except Exception as e:
        print('Error connecting to MQTT broker:', e)
        return None

def read_modbus_registers(modbus_client):
    try:
        modbus_values = modbus_client.read_holding_registers(slave_addr=MODBUS_DEVICE_ID, starting_addr=MODBUS_READ_REGISTER_ADDRESS, register_qty=MODBUS_READ_REGISTER_COUNT)
        return modbus_values
    except Exception as e:
        print('Error reading Modbus registers:', e)
        return None

def publish_to_mqtt(mqtt_client, modbus_values, topic):
    try:
        mqtt_client.publish(topic, str(modbus_values))
        #print(f'Published Modbus value {modbus_values} to topic: {topic}')
    except Exception as e:
        print('Error publishing to MQTT broker:', e)

def main():
    # Connect to WiFi
    station = connect_to_wifi()
    if station is None or not station.isconnected():
        print("Failed to connect to WiFi. Exiting.")
        return

    # Connect to MQTT broker
    mqtt_client = connect_to_mqtt()
    if mqtt_client is None:
        print("Failed to connect to MQTT broker. Exiting.")
        return

    # Create Modbus client instance
    modbus_client = ModbusTCPMaster(slave_ip=MODBUS_TCP_IP, slave_port=MODBUS_TCP_PORT, timeout=5)
    if modbus_client is None:
        print("Failed to create Modbus client instance. Exiting.")
        return

    while True:
        # Read Modbus registers
        modbus_values = read_modbus_registers(modbus_client)
        if modbus_values is None:
            print("Failed to read Modbus registers. Skipping this iteration.")
            time.sleep(1)
            continue
        
        # Publish each Modbus register value to its corresponding MQTT topic
        for i, value in enumerate(modbus_values):
            topic = f"Pico_W/Modbus/HR{MODBUS_READ_REGISTER_ADDRESS + i}"  # Adjust the topic naming according to your needs
            publish_to_mqtt(mqtt_client, value, topic)
        
        # Check for incoming MQTT messages
        mqtt_client.check_msg()
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
