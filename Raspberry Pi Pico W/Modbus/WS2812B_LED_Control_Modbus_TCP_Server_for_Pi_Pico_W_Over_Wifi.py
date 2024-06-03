from umodbus.tcp import ModbusTCP
import time
from machine import Pin
import network
from neopixel import NeoPixel

# Connect to a network
station = network.WLAN(network.STA_IF)
if station.active() and station.isconnected():
    station.disconnect()
    time.sleep(1)
station.active(False)
time.sleep(1)
station.active(True)

# Connect to WiFi
station.connect('Capgemini_4G', 'MN704116')
time.sleep(1)

while True:
    print('Waiting for WiFi connection...')
    if station.isconnected():
        print(f'Connected to WiFi, Pico W IP : {station.ifconfig()[0]}')
        break
    time.sleep(2)

# Modbus TCP parameters
tcp_port = 502
local_ip = station.ifconfig()[0]

# Setup WS2812B LEDs
NUM_LEDS = 10
PIN_LED = 16  # Pin for WS2812B LED
led = NeoPixel(Pin(PIN_LED), NUM_LEDS)

# Modbus TCP client
client = ModbusTCP()
is_bound = False

# Check whether client has been bound to an IP and port
is_bound = client.get_bound_status()

if not is_bound:
    client.bind(local_ip=local_ip, local_port=tcp_port)

# Callback function to control WS2812B LEDs based on register value
def LED_cb(reg_type, address, val):
    led_index = address  # Adjust the index to start from 0
    if val[0] == 1:
        led[led_index] = (0, 255, 0)  # Green color
    elif val[0] == 2:
        led[led_index] = (255, 0, 0)  # Red color
    else:
        led[led_index] = (0, 0, 0)  # Turn off LED
    led.write()

# Define register definitions for 10 LEDs
register_definitions = {
    "HREGS": {
        f"LED_{i}": {"register": i, "len": 1, "val": 0, "on_set_cb": LED_cb, "on_get_cb": LED_cb}
        for i in range(NUM_LEDS)
    }
}

# Setup Modbus registers
print('Setting up registers ...')
client.setup_registers(registers=register_definitions)
print('Register setup done')
print('Serving as TCP client on {}:{}'.format(local_ip, tcp_port))

# Main loop to process Modbus requests
while True:
    try:
        result = client.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP client...')
        break
#    except Exception as e:
#        print('Exception during execution: {}'.format(e))

print("Finished providing/accepting data as client")
