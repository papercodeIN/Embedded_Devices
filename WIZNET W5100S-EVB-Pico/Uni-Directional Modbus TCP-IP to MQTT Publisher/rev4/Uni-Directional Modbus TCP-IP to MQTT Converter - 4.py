import json
import uasyncio as asyncio
from umqtt.simple import MQTTClient
from umodbus.tcp import TCP as ModbusTCPMaster
from machine import Pin, SPI
import network
import time

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

async def connect_to_mqtt(mqtt_config):
    try:
        mqtt_client = MQTTClient(client_id='{MQTT_client_id}', server=mqtt_config['broker']['ip'], port=mqtt_config['broker']['port'], keepalive=30)
        mqtt_client.connect()
        print('Connected to MQTT broker')
        return mqtt_client
    except Exception as e:
        print('Error connecting to MQTT broker:', e)
        return None

async def publish_to_mqtt(mqtt_client, mqtt_config, payload, topic_prefix):
    try:
        mqtt_client.publish(f"{mqtt_config['baseTopic']}/{topic_prefix}", json.dumps(payload))
        #print(f'Published {payload} to topic: {mqtt_config["baseTopic"]}/{topic_prefix}')
    except Exception as e:
        print('Error publishing to MQTT broker:', e)


async def read_modbus_registers(modbus_client, modbus_config, register):
    try:
        if register['type'] == 'holding':
            registers = modbus_client.read_holding_registers(slave_addr=modbus_config['slaveID'], starting_addr=register['startAddress'], register_qty=register['endAddress'] - register['startAddress'] + 1)
        elif register['type'] == 'input':
            registers = modbus_client.read_input_registers(slave_addr=modbus_config['slaveID'], starting_addr=register['startAddress'], register_qty=register['endAddress'] - register['startAddress'] + 1)
        return registers
    except Exception as e:
        print(f'Error reading {register["type"]} registers from address {register["startAddress"]} to {register["endAddress"]}: {e}')
        return None


async def modbus_task(modbus_client, mqtt_client, mqtt_config, modbus_config):
    register_data = {}  # Dictionary to accumulate register data

    while True:
        for register in modbus_config['registers']:
            registers = await read_modbus_registers(modbus_client, modbus_config, register)
            if registers is not None:
                # Update the register_data dictionary with the new register values
                for tag, value in zip(register['tags'], registers):
                    register_data[tag] = value

        # Check if all registers have been read
        if len(register_data) == sum(len(register['tags']) for register in modbus_config['registers']):
            # Publish all register data at once
            await publish_to_mqtt(mqtt_client, mqtt_config, register_data, 'all_data')
            # Reset register_data for the next iteration
            register_data = {}

        await asyncio.sleep(0.5)



async def main():
    # Load configuration from JSON file
    with open('modbus_config.json') as config_file:
        config = json.load(config_file)
        mqtt_config = config['mqtt']
        modbus_config = config['modbus']

    # Initialize W5x00 chip
    nic = w5x00_init()
    if nic is None:
        return

    # Connect to MQTT broker
    mqtt_client = await connect_to_mqtt(mqtt_config)
    if mqtt_client is None:
        print("Failed to connect to MQTT broker. Exiting.")
        return

    # Create Modbus client instance
    modbus_client = ModbusTCPMaster(slave_ip=modbus_config['ip'], slave_port=modbus_config['port'], timeout=5)
    if modbus_client is None:
        print("Failed to create Modbus client instance. Exiting.")
        return

    await modbus_task(modbus_client, mqtt_client, mqtt_config, modbus_config)

if __name__ == "__main__":
    asyncio.run(main())
