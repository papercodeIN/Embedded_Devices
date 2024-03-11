from umodbus.serial import Serial as ModbusRTUMaster
from machine import Pin
host = ModbusRTUMaster(uart_id=0,baudrate=115200, data_bits=8, stop_bits=1, parity=None, pins=(Pin(0), Pin(1)), ctrl_pin=15)
#modbus_host = ModbusRTUMaster(uart_id=0,baudrate=115200,pins=(Pin(0), Pin(1)))
host.read_coils(slave_addr=1, starting_addr=0, coil_qty=16)
