import time
import threading
import RPi.GPIO as GPIO
import pigpio

# Pin definitions
sensor1Pin = 2
sensor2Pin = 3
lightPin = 18

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1Pin, GPIO.IN)
GPIO.setup(sensor2Pin, GPIO.IN)

# light pin dims through PWM
light = pigpio.pi()
light.set_PWM_frequency(lightPin, 1000)  # Set to 1000 Hz
light.set_PWM_dutycycle(lightPin, 0)  # 50% brightness

def fadeLightToDest():
  global lightValue
  global destLightValue
  if lightValue < destLightValue:
    lightValue += 1
  elif lightValue > destLightValue:
    lightValue -= 1
  light.set_PWM_dutycycle(lightPin, lightValue)
  

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
      
    fadeLightToDest()
    time.sleep(0.1)
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()
  lightPwm.stop()
  pwm_thread.join()