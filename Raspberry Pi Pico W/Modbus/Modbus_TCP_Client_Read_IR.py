import time
from umodbus.tcp import TCP as ModbusTCPMaster
import network

# ===============================================
# connect to a network
station = network.WLAN(network.STA_IF)
if station.active() and station.isconnected():
    station.disconnect()
    time.sleep(1)
station.active(False)
time.sleep(1)
station.active(True)

# station.connect('SSID', 'PASSWORD')
station.connect('Fusion Automate', 'Fusion_Automate')
time.sleep(1)

while True:
    print('Waiting for WiFi connection...')
    if station.isconnected():
        print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')
        break
    time.sleep(2)
# ===============================================

# TCP Slave setup
port = 502            # port to listen to
slave_addr = 1        # bus address of modbus_client
ireg_address = 0      # Input Status Adress
register_qty = 10     # Input Status Quantity to Read in Single Request

# IP Address of Modbus TCP Server
ip = '192.168.29.221'

# Setup Modbus TCP Client
modbus_client = ModbusTCPMaster(slave_ip=ip,slave_port=port,timeout=5)
print(f'Requesting data from Modbus TCP Server at {ip}:{port}')

register_value = modbus_client.read_input_registers(slave_addr=slave_addr,starting_addr=ireg_address,register_qty=register_qty)
print('Status of IREG from {} to {} : {}'.format(ireg_address, ireg_address+register_qty, register_value))
