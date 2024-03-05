from machine import Pin
import time, network
import os
os.chdir('/Raspberry PI Pico W/Telegram')
import utelegram

# telegram API key
telegram_api_key = ""

led = Pin("LED", Pin.OUT)

# Wifi Credentials and Wifi Conenctions
ssid = ''
pswd = ''

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pswd)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")
print(wlan.ifconfig())

def get_message(message):
    bot.send(message['message']['chat']['id'], "Hey!, Pi Pico didn't understand it.")

def reply_ping(message):
    print("Ping Test Command Received")
    bot.send(message['message']['chat']['id'], 'Hey!, Pi Pico is Up & Running')
    
    
# change led status with given parameters in message text
def led_cb(message):
    print("LED Control Command Received")
    if message['message']['text'] == '/ledon':
        led.on()
        bot.send(message['message']['chat']['id'], "LED IS ON")
    if message['message']['text'] == '/ledoff':
        led.off()
        bot.send(message['message']['chat']['id'], "LED IS OFF")
      
    
# start telegram bot 
bot = utelegram.ubot(telegram_api_key)
bot.register('/ping', reply_ping)       # ping message callback
bot.register('/ledon', led_cb)          # led message callback
bot.register('/ledoff', led_cb)         # led message callback
bot.set_default_handler(get_message)    # default message callback
bot.listen()