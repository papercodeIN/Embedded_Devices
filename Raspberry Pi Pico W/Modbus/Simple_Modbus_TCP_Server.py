from umodbus.tcp import ModbusTCP
import time
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

tcp_port = 502
local_ip = station.ifconfig()[0]

# ModbusTCP can get TCP requests from a host device to provide/set data
client = ModbusTCP()
is_bound = False

# check whether client has been bound to an IP and port
is_bound = client.get_bound_status()

if not is_bound:
    client.bind(local_ip=local_ip, local_port=tcp_port)

# commond slave register setup, to be used with the Master example above
register_definitions = \
        {'ISTS': {'EXAMPLE_ISTS': {'val': 1, 'register': 0, 'len': 1}},
         'IREGS': {'EXAMPLE_IREG': {'val': 1, 'register': 0, 'len': 1}},
         'HREGS': {'EXAMPLE_HREG0': {'val': 0, 'register': 0, 'len': 1},
                   'EXAMPLE_HREG1': {'val': 1, 'register': 1, 'len': 1},
                   'EXAMPLE_HREG2': {'val': 2, 'register': 2, 'len': 1},
                   'EXAMPLE_HREG3': {'val': 3, 'register': 3, 'len': 1},
                   'EXAMPLE_HREG4': {'val': 4, 'register': 4, 'len': 1}},
         'COILS': {'EXAMPLE_COIL0': {'val': 1, 'register': 0, 'len': 1},
                   'EXAMPLE_COIL1': {'val': 1, 'register': 1, 'len': 1}}}

print('Setting up registers ...')
client.setup_registers(registers=register_definitions)
print('Register setup done')
print('Serving as TCP client on {}:{}'.format(local_ip, tcp_port))

while True:
    try:
        result = client.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP client...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))

print("Finished providing/accepting data as client")
