import network
from umqtt.simple import MQTTClient
from umodbus.tcp import TCP as ModbusTCPMaster
from machine import Pin, SPI
import time

# Define constants
MQTT_BROKER = '192.168.1.23'
MQTT_PORT = 1883
MODBUS_TCP_IP = '192.168.1.23'
MODBUS_TCP_PORT = 502
MQTT_PUBLISH_TOPIC = 'Pico_W/Modbus/HR'
MODBUS_DEVICE_ID = 1
MODBUS_READ_REGISTER_ADDRESS = 0
MODBUS_READ_REGISTER_COUNT = 10


# W5x00 chip init
def w5x00_init():
    try:
        spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
        nic = network.WIZNET5K(spi, Pin(17), Pin(20))  # spi, cs, reset pin
        nic.active(True)
        nic.ifconfig(('192.168.1.20', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
        while not nic.isconnected():
            time.sleep(1)
            print("Waiting for W5x00 chip to connect...")
        print("W5x00 chip connected.")
        print("W5x00 chip ifconfig:", nic.ifconfig())
        return nic
    except Exception as e:
        print("Error initializing W5x00 chip:", e)
        return None

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

    # Initialize W5x00 chip
    nic = w5x00_init()
    if nic is None:
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