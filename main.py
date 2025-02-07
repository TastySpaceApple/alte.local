import time

import RPi.GPIO as GPIO

# Pin definitions
sensor1Pin = 2
sensor2Pin = 3
lightPin = 4

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1Pin, GPIO.IN)
GPIO.setup(sensor2Pin, GPIO.IN)
GPIO.setup(lightPin, GPIO.OUT)

try:
  while True:
    if GPIO.input(sensor1Pin) == GPIO.HIGH:
      print("Pin 1 is HIGH")
    if GPIO.input(sensor2Pin) == GPIO.HIGH:
      print("Pin 2 is HIGH")
    if GPIO.input(sensor1Pin) == GPIO.HIGH and GPIO.input(sensor2Pin) == GPIO.HIGH:
      GPIO.output(lightPin, GPIO.HIGH)
    else:
      GPIO.output(lightPin, GPIO.LOW)
    time.sleep(0.1)
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()