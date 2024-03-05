# import modbus host classes
from umodbus.tcp import ModbusTCP
from umqtt.simple import MQTTClient
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
# Define MQTT Broker credentials
MQTT_BROKER_IP = '192.168.29.221'
MQTT_BROKER_PORT = 1883
MQTT_CLIENT_ID = 'Pico_W_Mqtt_Client'
MQTT_TOPIC = 'Pico_W/Modbus'
# ===============================================
# Define MQTT client
mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER_IP, MQTT_BROKER_PORT,keepalive=30)
mqtt_client.connect()
# ===============================================
# TCP Slave setup
tcp_port = 502
local_ip = station.ifconfig()[0]
# ===============================================
# ModbusTCP can get TCP requests from a host device to provide/set data
client = ModbusTCP()
is_bound = False
# check whether client has been bound to an IP and port
is_bound = client.get_bound_status()
if not is_bound:
    client.bind(local_ip=local_ip, local_port=tcp_port)
# ===============================================

def my_coil_set_cb(reg_type, address, val):
    mqtt_client.publish(MQTT_TOPIC+"/"+str(reg_type)+" / "+str(address), str(int(val[0])))
    print('Custom callback, called on setting {} at {} to: {}'.
          format(reg_type, address, val))


def my_coil_get_cb(reg_type, address, val):
    mqtt_client.publish(MQTT_TOPIC+"/"+str(reg_type)+" / "+str(address), str(int(val[0])))
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


def my_holding_register_set_cb(reg_type, address, val):
    mqtt_client.publish(MQTT_TOPIC+"/"+str(reg_type)+" / "+str(address), str(val[0]))
    print('Custom callback, called on setting {} at {} to: {}'.
          format(reg_type, address, val[0]))


def my_holding_register_get_cb(reg_type, address, val):
    mqtt_client.publish(MQTT_TOPIC+"/"+str(reg_type)+" / "+str(address), str(val[0]))
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val[0]))


def my_discrete_inputs_register_get_cb(reg_type, address, val):
    mqtt_client.publish(MQTT_TOPIC+"/"+str(reg_type)+" / "+str(address), str(int(val[0])))
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


def my_inputs_register_get_cb(reg_type, address, val):
    # usage of global isn't great, but okay for an example
    global client

    mqtt_client.publish(MQTT_TOPIC+"/"+str(reg_type)+" / "+str(address), str(int(val[0])))
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))

    # any operation should be as short as possible to avoid response timeouts
    new_val = val[0] + 1
    
    client.set_ireg(address=address, value=new_val)
    print('Incremented current value by +1 before sending response')


# commond slave register setup, to be used with the Master example above
register_definitions = {
'ISTS': {'EXAMPLE_ISTS': {'val': 0, 'register': 0, 'len': 1}},
'IREGS': {'EXAMPLE_IREG': {'val': 0, 'register': 0, 'len': 1}},
'HREGS': {'EXAMPLE_HREG': {'val': 0, 'register': 0, 'len': 1}},
'COILS': {'EXAMPLE_COIL': {'val': 0, 'register': 0, 'len': 1}}}

register_definitions['COILS']['EXAMPLE_COIL']['on_set_cb'] = my_coil_set_cb
register_definitions['COILS']['EXAMPLE_COIL']['on_get_cb'] = my_coil_get_cb
register_definitions['HREGS']['EXAMPLE_HREG']['on_set_cb'] = my_holding_register_set_cb
register_definitions['HREGS']['EXAMPLE_HREG']['on_get_cb'] = my_holding_register_get_cb
register_definitions['ISTS']['EXAMPLE_ISTS']['on_get_cb'] = my_discrete_inputs_register_get_cb
register_definitions['IREGS']['EXAMPLE_IREG']['on_get_cb'] = my_inputs_register_get_cb

print('Setting up registers ...')
client.setup_registers(registers=register_definitions)
print('Register setup done')
print('Serving as TCP client on {}:{}'.format(local_ip, tcp_port))

while True:
    try:
        result = client.process()
    except KeyboardInterrupt:
        mqtt_client.disconnect()
        print('KeyboardInterrupt, stopping TCP client...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))

print("Finished providing/accepting data as client")
