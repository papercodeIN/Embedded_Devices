import network
from umqtt.simple import MQTTClient
from umodbus.tcp import TCP as ModbusTCPMaster
from machine import Pin, SPI
import uasyncio as asyncio
import json
import time

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

async def connect_to_mqtt(mqtt_config):
    mqtt_client = MQTTClient(client_id='{MQTT_client_id}', server=mqtt_config['broker'], port=mqtt_config['port'], keepalive=30)
    try:
        mqtt_client.connect()
        print('Connected to MQTT broker')
        return mqtt_client
    except Exception as e:
        print('Error connecting to MQTT broker:', e)
        return None

async def read_modbus_registers(modbus_client, function_code, ranges, modbus_config):
    results = []
    for range in ranges:
        start = range["start"]
        count = range["length"]
        try:
            if function_code == 3:
                registers = modbus_client.read_holding_registers(slave_addr=modbus_config['device_id'], starting_addr=start, register_qty=count)
            elif function_code == 4:
                registers = modbus_client.read_input_registers(slave_addr=modbus_config['device_id'], starting_addr=start, register_qty=count)
            results.append((start, registers))
        except Exception as e:
            print(f'Error reading Modbus registers from address {start} with length {count}: {e}')
            results.append((start, None))
    return results

async def publish_to_mqtt(mqtt_client, modbus_values, topic_prefix):
    try:
        for start, values in modbus_values:
            if values is not None:
                for i, value in enumerate(values):
                    topic = f"{topic_prefix}{start + i}"
                    mqtt_client.publish(topic, str(value))
                    # print(f'Published {value} to topic: {topic}')
    except Exception as e:
        print('Error publishing to MQTT broker:', e)

async def main():
    # Load configuration from JSON file
    with open('modbus_config.json') as config_file:
        config = json.load(config_file)
        mqtt_config = config['mqtt']
        modbus_config = config['modbus']
        holding_register_ranges = config["holding_registers"]
        input_register_ranges = config["input_registers"]

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
    modbus_client = ModbusTCPMaster(slave_ip=modbus_config['tcp_ip'], slave_port=modbus_config['tcp_port'], timeout=5)
    if modbus_client is None:
        print("Failed to create Modbus client instance. Exiting.")
        return

    async def modbus_task():
        while True:
            # Read and publish Modbus holding registers
            modbus_holding_registers = await read_modbus_registers(modbus_client, 3, holding_register_ranges, modbus_config)
            await publish_to_mqtt(mqtt_client, modbus_holding_registers, 'Pico_W/Modbus/HoldingRegisters/')

            # Read and publish Modbus input registers
            modbus_input_registers = await read_modbus_registers(modbus_client, 4, input_register_ranges, modbus_config)
            await publish_to_mqtt(mqtt_client, modbus_input_registers, 'Pico_W/Modbus/InputRegisters/')

            await asyncio.sleep(0.5)

    async def mqtt_task():
        while True:
            mqtt_client.check_msg()
            await asyncio.sleep(0.1)

    await asyncio.gather(modbus_task(), mqtt_task())

if __name__ == "__main__":
    asyncio.run(main())
