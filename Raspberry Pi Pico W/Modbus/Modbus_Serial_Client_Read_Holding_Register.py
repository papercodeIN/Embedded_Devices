from umodbus.serial import Serial
from machine import UART
from machine import Pin
import struct
import time
import machine

m=Serial(uart_id=0)

print(m._uart)
slave_addr=0x01
starting_address=0x01
register_quantity=4
signed=True
while 1:
  register_value = m.read_holding_registers(slave_addr, starting_address, register_quantity, signed)
  print('Holding register value: ' + ' '.join('{:d}'.format(x) for x in register_value))
  time.sleep(1)
  #break
