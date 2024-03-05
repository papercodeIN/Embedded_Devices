import network
from umqtt.simple import MQTTClient
from umodbus.tcp import TCP as ModbusTCPMaster
import time

# Define constants
MQTT_BROKER = '192.168.1.5'
MQTT_PORT = 1883
MODBUS_TCP_IP = '192.168.1.5'
MODBUS_TCP_PORT = 502
WIFI_SSID = 'Capgemini_4G'
WIFI_PASSWORD = 'MN704116'

# Define Modbus device IDs, register addresses, and count for each device
MODBUS_DEVICE_IDS = [1, 2, 3]  # Example device IDs
MODBUS_READ_REGISTER_ADDRESSES = [0, 0, 0]  # Example register addresses
MODBUS_READ_REGISTER_COUNTS = [10, 10, 10]  # Example register counts

# Define MQTT publish topic
MQTT_PUBLISH_TOPIC = 'Pico_W/Modbus/'

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

def read_modbus_register(modbus_client, device_id, register_address):
    try:
        modbus_value = modbus_client.read_holding_registers(slave_addr=device_id, starting_addr=register_address, register_qty=1)[0]
        return modbus_value
    except Exception as e:
        print(f'Error reading Modbus register for device {device_id}, address {register_address}:', e)
        return None

def publish_to_mqtt(mqtt_client, modbus_value, topic):
    try:
        mqtt_client.publish(topic, str(modbus_value))
        #print(f'Published Modbus value {modbus_value} to topic: {topic}')
    except Exception as e:
        print('Error publishing to MQTT broker:', e)

def main():
    global MQTT_PUBLISH_TOPIC
    
    # Connect to WiFi
    station = connect_to_wifi()

    # Connect to MQTT broker
    mqtt_client = connect_to_mqtt()
    if mqtt_client is None:
        return

    # Create Modbus client instance
    modbus_client = ModbusTCPMaster(slave_ip=MODBUS_TCP_IP, slave_port=MODBUS_TCP_PORT, timeout=5)

    while True:
        for device_id, register_address, register_count in zip(MODBUS_DEVICE_IDS, MODBUS_READ_REGISTER_ADDRESSES, MODBUS_READ_REGISTER_COUNTS):
            for register_offset in range(register_count):
                # Read Modbus register for each device
                register_value = read_modbus_register(modbus_client, device_id, register_address + register_offset)
                if register_value is not None:
                    # Publish Modbus register value to MQTT for each device
                    topic = f"{MQTT_PUBLISH_TOPIC}/{device_id}/HR{register_address + register_offset}"
                    publish_to_mqtt(mqtt_client, register_value, topic)
                else:
                    print(f"Failed to read Modbus register for device {device_id}, address {register_address + register_offset}")
        
        # Check for incoming MQTT messages
        mqtt_client.check_msg()
        
        time.sleep(5)

if __name__ == "__main__":
    main()
