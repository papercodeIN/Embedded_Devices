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
hreg_address = 5      # Holding Register Address

# IP Address of Modbus TCP Server
ip = '192.168.29.221'

# Setup Modbus TCP Client
modbus_client = ModbusTCPMaster(slave_ip=ip,slave_port=port,timeout=5)
print(f'Updating data to Modbus TCP Server at {ip}:{port}')
       
# WRITE HREGS
new_hreg_val = 44
operation_status = modbus_client.write_single_register(slave_addr=slave_addr,register_address=hreg_address,register_value=new_hreg_val)
print('Result of setting HREG {}: {}'.format(hreg_address, operation_status))
