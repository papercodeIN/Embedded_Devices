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
starting_addr = 0     # starting addres of register
register_qty = 5      # number of regsiter to read

# IP Address of Modbus TCP Server
ip = '192.168.29.221'

# Setup Modbus TCP Client
modbus_client = ModbusTCPMaster(slave_ip=ip,slave_port=port,timeout=5)
print(f'Requesting data from Modbus TCP Server at {ip}:{port}')
       
# READ HREGS
register_value = modbus_client.read_holding_registers(slave_addr=slave_addr,starting_addr=starting_addr,register_qty=register_qty)
print('Status of HREG from {} to {} : {}'.format(starting_addr,starting_addr + register_qty, register_value))

