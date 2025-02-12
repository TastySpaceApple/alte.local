import time

import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
pin = 3
GPIO.setup(pin, GPIO.IN)

try:
  while True:
    value = GPIO.input(pin)
    print(f"Pin {pin} value: {value}")
    time.sleep(1)
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()