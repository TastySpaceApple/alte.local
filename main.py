import time

import RPi.GPIO as GPIO

# Pin definitions
pin1 = 2
pin2 = 3

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin1, GPIO.IN)
GPIO.setup(pin2, GPIO.IN)

try:
  while True:
    if GPIO.input(pin1) == GPIO.HIGH:
      print("Pin 1 is HIGH")
    if GPIO.input(pin2) == GPIO.HIGH:
      print("Pin 2 is HIGH")
    time.sleep(0.1)
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()