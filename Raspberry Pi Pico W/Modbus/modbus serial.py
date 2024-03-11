from umodbus.serial import Serial as ModbusRTUMaster
from machine import Pin
host = ModbusRTUMaster(uart_id=0,baudrate=115200, data_bits=8, stop_bits=1, parity=None, pins=(Pin(0), Pin(1)), ctrl_pin=15)
#modbus_host = ModbusRTUMaster(uart_id=0,baudrate=115200,pins=(Pin(0), Pin(1)))
host.read_coils(slave_addr=1, starting_addr=0, coil_qty=16)

#=============================================================================================================================

import time
from machine import Pin, UART
from umodbus.serial import Serial as ModbusRTUMaster
rtu_pins = (Pin(0), Pin(1))
address = 0
qty = 3
#host = ModbusRTUMaster(uart_id=0,baudrate = 9600, pins=rtu_pins)
host = ModbusRTUMaster(baudrate=9600, data_bits=8, stop_bits=1, parity=None, pins=rtu_pins, ctrl_pin=None, uart_id =0)
print('HOLDING REGISTER request test.')
print('Reading qty={} from address {}:'.format(qty, address))
values = host.read_holding_registers(slave_addr=1, starting_addr=address, register_qty=qty, signed=False)
print('Result: {}'.format(values))

