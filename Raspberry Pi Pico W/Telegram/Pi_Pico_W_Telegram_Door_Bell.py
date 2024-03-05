import network
import ubinascii
from machine import Pin
import urequests as requests
import time


ssid = ''
pw = ''
botToken = ''
chatId = ''
startupText = 'Pico started!'
text = 'Door bell activated!'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

led = Pin('LED', Pin.OUT)

# See the MAC address in the wireless chip OTP
print('mac = ' + ubinascii.hexlify(network.WLAN().config('mac'),':').decode())


# Telegram send message URL
sendURL = 'https://api.telegram.org/bot' + botToken + '/sendMessage'
    
# Send a telegram message to a given user id
def send_message (chatId, message):
    response = requests.post(sendURL + "?chat_id=" + str(chatId) + "&text=" + message)
    # Close to avoid filling up the RAM.
    response.close()

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
        
def is_wifi_connected():
    wlan_status = wlan.status()
    if wlan_status != 3:
        return False
    else:
        return True

def connect_wifi():
    while True:
        if (is_wifi_connected()):
            blink_onboard_led(3)
            led.on()
            print('ip = ' + wlan.ifconfig()[0])
            send_message(chatId, startupText)
            break
        else:
            print('WiFi is disconnected. Trying to connect.')
            led.off()
            wlan.connect(ssid, pw)
            time.sleep(3)

# Connect to WiFi
connect_wifi()

# Setup GPIO pins
doorBellInput = Pin(18, Pin.IN, Pin.PULL_DOWN)
loopDelay = 0.25
buttonDelay = 5

while True:
    try:
        if (not is_wifi_connected()):
            connect_wifi()
        
        if (doorBellInput.value() == 1):
            print('Door bell pressed!')
            send_message(chatId, text)
            time.sleep(buttonDelay)
        
        time.sleep(loopDelay)
        
    except OSError as e:
        print(e)
        led.off()
        wlan.disconnect()
        # Grace period.
        time.sleep(10)
        led.on()
        pass