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
coil_address = 0      # Starting Coil Address

# IP Address of Modbus TCP Server
ip = '192.168.29.221'

# Setup Modbus TCP Client
modbus_client = ModbusTCPMaster(slave_ip=ip,slave_port=port,timeout=5)
print(f'Updating data to Modbus TCP Server at {ip}:{port}')

# WRITE COILS
new_coil_val = 0
operation_status = modbus_client.write_single_coil(slave_addr=slave_addr,output_address=coil_address,output_value=new_coil_val)
print('Result of setting COIL {}: {}'.format(coil_address, operation_status))
