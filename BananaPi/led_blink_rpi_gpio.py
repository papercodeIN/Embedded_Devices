import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set up the GPIO pin for the LED
LED_PIN = 7
GPIO.setup(LED_PIN, GPIO.OUT)

# Function to blink the LED
def blink_led():
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
        time.sleep(1)                    # Wait for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn off the LED
        time.sleep(1)                    # Wait for 1 second

try:
    blink_led()
except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up the GPIO pins on interrupt
