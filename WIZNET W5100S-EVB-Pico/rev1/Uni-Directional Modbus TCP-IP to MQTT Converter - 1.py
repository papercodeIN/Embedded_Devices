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
MODBUS_DEVICE_ID = 1
MODBUS_READ_LENGTH = 10

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

# def read_modbus_coils(modbus_client):
#     try:
#         coils = modbus_client.read_coils(slave_addr=MODBUS_DEVICE_ID, starting_addr=0, register_qty=MODBUS_READ_LENGTH)
#         return coils
#     except Exception as e:
#         print('Error reading Modbus coils:', e)
#         return None

# def read_modbus_discrete_inputs(modbus_client):
#     try:
#         discrete_inputs = modbus_client.read_discrete_inputs(slave_addr=MODBUS_DEVICE_ID, starting_addr=0, quantity=MODBUS_READ_LENGTH)
#         return discrete_inputs
#     except Exception as e:
#         print('Error reading Modbus discrete inputs:', e)
#         return None

def read_modbus_input_registers(modbus_client):
    try:
        input_registers = modbus_client.read_input_registers(slave_addr=MODBUS_DEVICE_ID, starting_addr=0, register_qty=MODBUS_READ_LENGTH)
        return input_registers
    except Exception as e:
        print('Error reading Modbus input registers:', e)
        return None

def read_modbus_holding_registers(modbus_client):
    try:
        holding_registers = modbus_client.read_holding_registers(slave_addr=MODBUS_DEVICE_ID, starting_addr=0, register_qty=MODBUS_READ_LENGTH)
        return holding_registers
    except Exception as e:
        print('Error reading Modbus holding registers:', e)
        return None

def publish_to_mqtt(mqtt_client, modbus_values, topic_prefix):
    try:
        for i, value in enumerate(modbus_values):
            topic = f"{topic_prefix}{i}"
            mqtt_client.publish(topic, str(value))
            #print(f'Published {value} to topic: {topic}')
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
        # # Read Modbus coils
        # modbus_coils = read_modbus_coils(modbus_client)
        # if modbus_coils is not None:
        #     publish_to_mqtt(mqtt_client, modbus_coils, 'Pico_W/Modbus/Coils/')

        # # Read Modbus discrete inputs
        # modbus_discrete_inputs = read_modbus_discrete_inputs(modbus_client)
        # if modbus_discrete_inputs is not None:
        #     publish_to_mqtt(mqtt_client, modbus_discrete_inputs, 'Pico_W/Modbus/DiscreteInputs/')

        # Read Modbus input registers
        modbus_input_registers = read_modbus_input_registers(modbus_client)
        if modbus_input_registers is not None:
            publish_to_mqtt(mqtt_client, modbus_input_registers, 'Pico_W/Modbus/InputRegisters/')

        # Read Modbus holding registers
        modbus_holding_registers = read_modbus_holding_registers(modbus_client)
        if modbus_holding_registers is not None:
            publish_to_mqtt(mqtt_client, modbus_holding_registers, 'Pico_W/Modbus/HoldingRegisters/')
        
        # Check for incoming MQTT messages
        mqtt_client.check_msg()
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()

