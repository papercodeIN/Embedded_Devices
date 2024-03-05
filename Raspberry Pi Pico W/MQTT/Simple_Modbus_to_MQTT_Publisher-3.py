import time
from umodbus.tcp import TCP as ModbusTCPMaster
import network
from umqtt.simple import MQTTClient
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
port = 502            # port to listen to
slave_addr = 1        # bus address of modbus_client
# IP Address of Modbus TCP Server
ip = '192.168.29.221'
# register_numbers = [0,2,4,6,8]
coil_numbers = [0,2,4,6,8]
# ===============================================
# Setup Modbus TCP Client
modbus_client = ModbusTCPMaster(slave_ip=ip,slave_port=port,timeout=5)
print(f'Requesting data from Modbus TCP Server at {ip}:{port}')
# ===============================================

while True:
    try:
        # for i in range(len(register_numbers)):
        #     register_value = modbus_client.read_holding_registers(slave_addr=slave_addr,starting_addr=register_numbers[i],register_qty=1)
        #     mqtt_client.publish(MQTT_TOPIC + '/HR/' + str(register_numbers[i]), str(register_value[0]))
        for i in range(len(coil_numbers)):
            coil_value = modbus_client.read_coils(slave_addr=slave_addr,starting_addr=coil_numbers[i],coil_qty=1)
            mqtt_client.publish(MQTT_TOPIC + '/COIL/' + str(coil_numbers[i]), str(coil_value[0]))        
    except KeyboardInterrupt:
        mqtt_client.disconnect()
        print('KeyboardInterrupt, stopping TCP client...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))
