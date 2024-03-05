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
ist_address = 0       # Input Status Adress
input_qty = 1         # Input Status Quantity to Read in Single Request

# IP Address of Modbus TCP Server
ip = '192.168.29.221'

# Setup Modbus TCP Client
modbus_client = ModbusTCPMaster(slave_ip=ip,slave_port=port,timeout=5)
print(f'Updating data to Modbus TCP Server at {ip}:{port}')


# READ ISTS
input_status = modbus_client.read_discrete_inputs(slave_addr=slave_addr,starting_addr=ist_address,input_qty=input_qty)
print('Status of IST from {} to {} : {}'.format(ist_address, ist_address + input_qty,input_status))
