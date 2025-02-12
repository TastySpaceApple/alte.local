import time
import threading
import RPi.GPIO as GPIO
from audio_recorder import AudioRecorder 

recorder = AudioRecorder('http://atra-bce32f116e3f.herokuapp.com/alte')

# Pin definitions
sensor1Pin = 3
lightPin = 18

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1Pin, GPIO.IN)
GPIO.setup(lightPin, GPIO.OUT)

# Setup PWM for light pin
pwm = GPIO.PWM(lightPin, 1000)  # Set to 1000 Hz
pwm.start(0)  # Start with 0% duty cycle

lightValue = 0
destLightValue = 0

def lightEaseIn(value): # value is - to 255
  return int(255 * (value / 255) ** 2)

def fadeLightToDest():
  global lightValue
  global destLightValue
  if lightValue < destLightValue:
    lightValue += 1
  elif lightValue > destLightValue:
    lightValue -= 1
  pwm.ChangeDutyCycle(lightEaseIn(lightValue) / 255 * 100)
  time.sleep(0.01)

def fadeLightThread():
  while True:
    fadeLightToDest()

# Start the fadeLightToDest function in a separate thread
fade_thread = threading.Thread(target=fadeLightThread)
fade_thread.daemon = True
fade_thread.start()

window_size = 20
window_running_average_array = []
for i in range(window_size):
  window_running_average_array.append(0)

def window_running_average(newValue):
  global window_running_average_array
  window_running_average_array.append(newValue)
  if len(window_running_average_array) > window_size:
    window_running_average_array.pop(0)
  return sum(window_running_average_array) / len(window_running_average_array)

recorderLevel = 0

try:
  while True:    
    if recorder.isRecording:
      recorder.record()
      recorderLevel = window_running_average(recorder.level)
      
    sensor1Pressed = GPIO.input(sensor1Pin) == GPIO.LOW

    if sensor1Pressed:
      destLightValue = 255
      if not recorder.isRecording and lightValue == 255:
        recorder.open()
        print("Started Recording")      
    elif not sensor1Pressed:
      destLightValue = 0
      
      if recorder.isRecording and lightValue == 0:
        print("Stopped Recording")
        recorder.stop()
        recorder.save()
        if recorder.getRecordingDuration() > 15:
          threading.Thread(target=recorder.send).start()
          print("sending recording " + recorder.recording_filename)
          
except KeyboardInterrupt:
  pass
finally:
  pwm.stop()
  GPIO.cleanup()
  print("GPIO cleanup")
