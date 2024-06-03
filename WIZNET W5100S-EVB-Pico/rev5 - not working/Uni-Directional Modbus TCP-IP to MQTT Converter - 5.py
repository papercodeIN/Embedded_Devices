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

async def publish_to_mqtt(mqtt_client, mqtt_config, payload, slave):
    try:
        topic_prefix = f"{mqtt_config['baseTopic']}/slave{slave['id']}"
        mqtt_client.publish(topic_prefix, json.dumps(payload))
        print(f'Published {payload} to topic: {topic_prefix}')
    except Exception as e:
        print('Error publishing to MQTT broker:', e)


async def read_modbus_registers(modbus_client, slave):
    register_data = {}  # Dictionary to accumulate register data

    for register in slave['registers']:
        try:
            if register['type'] == 'holding':
                registers = modbus_client.read_holding_registers(slave['ip'], slave['port'], slave['id'], register['startAddress'], register['endAddress'] - register['startAddress'] + 1)
            elif register['type'] == 'input':
                registers = modbus_client.read_input_registers(slave['ip'], slave['port'], slave['id'], register['startAddress'], register['endAddress'] - register['startAddress'] + 1)
            # Update the register_data dictionary with the new register values
            for tag, value in zip(register['tags'], registers):
                register_data[tag] = value
        except Exception as e:
            print(f'Error reading {register["type"]} registers from address {register["startAddress"]} to {register["endAddress"]}: {e}')
    return register_data


async def modbus_task(modbus_client, mqtt_client, mqtt_config, modbus_config, slave):
    while True:
        register_data = await read_modbus_registers(modbus_client, slave)
        if register_data:
            await publish_to_mqtt(mqtt_client, mqtt_config, register_data, slave)
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

    # Create Modbus client instances for each slave
    modbus_clients = {}
    for slave in modbus_config['slaves']:
        try:
            modbus_clients[slave['id']] = ModbusTCPMaster(slave['ip'], slave['port'], timeout=5)
            print(f"Modbus client created for Slave ID {slave['id']}")
        except Exception as e:
            print(f"Failed to create Modbus client for Slave ID {slave['id']}: {e}")

    # Start modbus tasks for each slave
    modbus_tasks = []
    for slave_id, modbus_client in modbus_clients.items():
        for slave in modbus_config['slaves']:
            if slave['id'] == slave_id:
                task = asyncio.create_task(modbus_task(modbus_client, mqtt_client, mqtt_config, modbus_config, slave))
                modbus_tasks.append(task)

    # Run all modbus tasks concurrently
    await asyncio.gather(*modbus_tasks)

if __name__ == "__main__":
    asyncio.run(main())
