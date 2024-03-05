import utime
from machine import Pin
from umqtt.simple import MQTTClient

class InvalidChecksum(Exception):
    pass

class InvalidPulseCount(Exception):
    pass

MAX_UNCHANGED = 100
MIN_INTERVAL_US = 200000
HIGH_LEVEL = 50
EXPECTED_PULSES = 84

class DHT11:
    def __init__(self, pin):
        self._pin = pin
        self._last_measure = 0

    def measure(self):
        current_ticks = utime.ticks_us()
        if utime.ticks_diff(current_ticks, self._last_measure) < MIN_INTERVAL_US:
            return None, None
        
        try:
            self._send_init_signal()
            pulses = self._capture_pulses()
            buffer = self._convert_pulses_to_buffer(pulses)
            self._verify_checksum(buffer)

            temperature = buffer[2] + buffer[3] / 10
            humidity = buffer[0] + buffer[1] / 10
            self._last_measure = utime.ticks_us()

            return temperature, humidity
        except InvalidPulseCount:
            return None, None

    def _send_init_signal(self):
        self._pin.init(Pin.OUT, Pin.PULL_DOWN)
        self._pin.value(1)
        utime.sleep_ms(50)
        self._pin.value(0)
        utime.sleep_ms(18)

    def _capture_pulses(self):
        pin = self._pin
        pin.init(Pin.IN, Pin.PULL_UP)

        val = 1
        idx = 0
        transitions = bytearray(EXPECTED_PULSES)
        unchanged = 0
        timestamp = utime.ticks_us()

        while unchanged < MAX_UNCHANGED:
            if val != pin.value():
                if idx >= EXPECTED_PULSES:
                    raise InvalidPulseCount("Got more than {} pulses".format(EXPECTED_PULSES))
                now = utime.ticks_us()
                transitions[idx] = now - timestamp
                timestamp = now
                idx += 1

                val = 1 - val
                unchanged = 0
            else:
                unchanged += 1
        pin.init(Pin.OUT, Pin.PULL_DOWN)
        if idx != EXPECTED_PULSES:
            raise InvalidPulseCount("Expected {} but got {} pulses".format(EXPECTED_PULSES, idx))
        return transitions[4:]

    def _convert_pulses_to_buffer(self, pulses):
        binary = 0
        for idx in range(0, len(pulses), 2):
            binary = binary << 1 | int(pulses[idx] > HIGH_LEVEL)

        buffer = bytearray(5)
        for shift in range(4, -1, -1):
            buffer[4 - shift] = (binary >> shift * 8) & 0xFF
        return buffer

    def _verify_checksum(self, buffer):
        checksum = sum(buffer[:4]) & 0xFF
        if checksum != buffer[4]:
            raise InvalidChecksum()

# WiFi and MQTT Broker Configuration
WIFI_SSID = ""
WIFI_PASSWORD = ""
MQTT_BROKER = ""
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "Pico/Sensor/Temperature"
MQTT_TOPIC_HUMIDITY = "Pico/Sensor/Humidity"

def connect_to_wifi():
    import network
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(WIFI_SSID, WIFI_PASSWORD)
    while not station.isconnected():
        pass
    print("Connected to WiFi")

def connect_to_mqtt():
    client = MQTTClient("pico_client", MQTT_BROKER, MQTT_PORT)
    client.connect()
    print("Connected to MQTT Broker")
    return client

def main():
    connect_to_wifi()
    mqtt_client = connect_to_mqtt()

    pin = Pin(28, Pin.OUT)
    sensor = DHT11(pin)

    while True:
        temperature, humidity = sensor.measure()
        if temperature is not None and humidity is not None:
            print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))
            mqtt_client.publish(MQTT_TOPIC_TEMP, str(temperature))
            mqtt_client.publish(MQTT_TOPIC_HUMIDITY, str(humidity))
        utime.sleep(5)

if __name__ == "__main__":
    main()
