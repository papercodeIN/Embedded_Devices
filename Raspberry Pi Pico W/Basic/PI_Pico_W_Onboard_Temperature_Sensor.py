from machine import ADC
import time

class Temperature:
    def __init__(self):
        adcpin = 4
        self.sensor = ADC(adcpin)
        
    def ReadTemperature(self):
        adc_value = self.sensor.read_u16()
        volt = (3.3/65535)*adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        return round(temperature, 1)

sensor = Temperature()

while True:
    temperature = sensor.ReadTemperature()
    print(temperature)
    time.sleep(1)    