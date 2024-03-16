import time
from machine import Pin, UART
from umodbus.serial import Serial as ModbusRTUMaster

# Define the pins for Modbus communication
rtu_pins = (Pin(0), Pin(1))

# Define the starting address to read from
starting_address = 0

# Define the quantity of registers to read
qty = 3

# Initialize Modbus RTU Master
host = ModbusRTUMaster(baudrate=9600, data_bits=8, stop_bits=1, parity=None, pins=rtu_pins, ctrl_pin=None, uart_id=0)

# Continuous reading loop
while True:
    try:
        print('Reading qty={} from starting address {}:'.format(qty, starting_address))

        # Read holding registers from the slave device
        values = host.read_holding_registers(slave_addr=1, starting_addr=starting_address, register_qty=qty, signed=False)

        # Print the result
        print('Result: {}'.format(values))

    except Exception as e:
        print('An error occurred:', e)

    # Wait for 5 seconds before the next reading
    time.sleep(5)