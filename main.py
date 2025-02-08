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

# light pin dims through PWM
GPIO.setup(lightPin, GPIO.OUT)

lightPwm = GPIO.PWM(lightPin, 500)
lightPwm.start(0)

destLightValue = 0

def fadeLightLinearStep():
  global destLightValue
  if lightPwm._dc < destLightValue:
    lightPwm.ChangeDutyCycle(min(lightPwm._dc + 0.4, 100))
  elif lightPwm._dc > destLightValue:
    lightPwm.ChangeDutyCycle(max(lightPwm._dc - 0.4, 0))

try:
  while True:
    if GPIO.input(sensor1Pin) == GPIO.HIGH:
      print("Pin 1 is HIGH")
    if GPIO.input(sensor2Pin) == GPIO.HIGH:
      print("Pin 2 is HIGH")
    
    if GPIO.input(sensor1Pin) == GPIO.HIGH and GPIO.input(sensor2Pin) == GPIO.HIGH:
      destLightValue = 100
    else:
      destLightValue = 0
      
    fadeLightLinearStep()
    time.sleep(0.1)
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()