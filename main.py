import time
import threading
import RPi.GPIO as GPIO
import pigpio
from audio_recorder import AudioRecorder 

recorder = AudioRecorder('http://atra-bce32f116e3f.herokuapp.com/alte')

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

lightValue = 0
destLightValue = 0

countRecordingIntent = 0
recordingIntentThreshold = 200

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
    if recorder.isRecording:
      recorder.record()

    if GPIO.input(sensor1Pin) == GPIO.HIGH and GPIO.input(sensor2Pin) == GPIO.HIGH:
      destLightValue = 255
      countRecordingIntent = min(countRecordingIntent + 1, recordingIntentThreshold)
      if not recorder.isRecording and countRecordingIntent == recordingIntentThreshold:
        recorder.open()
        print("Started Recording")      
    else:
      destLightValue = 0
      countRecordingIntent = max(countRecordingIntent - 1, 0)
      print(countRecordingIntent)
      if recorder.isRecording and countRecordingIntent == 0:
        print("Stopped Recording")
        recorder.stop()
        if recorder.getRecordingDuration() > 5:
          recorder.save()
          recorder.send()
          print("sent")
      
    fadeLightToDest()
except KeyboardInterrupt:
  pass
finally:
  GPIO.cleanup()