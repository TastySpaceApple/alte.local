import time
import pyaudio
import wave
import requests
import audioop

chunk = 4096  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second

p = pyaudio.PyAudio()  # Create an interface to PortAudio
# https://www.programcreek.com/python/?code=samclane%2FLIFX-Control-Panel%2FLIFX-Control-Panel-master%2Flifx_control_panel%2Futilities%2Faudio.py
SCALE = 8  # Change if too dim/bright
EXPONENT = 2  # Change if too little/too much difference between loud and quiet sounds

class AudioRecorder:
  def __init__(self, upload_route):
    self.stream = None
    self.upload_route = upload_route
    self.isRecording = False
   
  def open(self):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    recording_filename = 'recordings/recording' + timestamp + '.wav'
    self.recording_filename = recording_filename
    self.stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk,
                  input=True)    
    self.frames = [] 
    self.startRecordingTime = time.time()
    self.isRecording = True

  def record(self):
    data = self.stream.read(chunk)
    rms = audioop.rms(data, 2)
    level = min(rms / (2.0 ** 16) * SCALE, 1.0)
    level = level ** EXPONENT
    level = int(level * 155) + 100
    self.level = level
    self.frames.append(data)

  def getRecordingDuration(self):
    return round(time.time() - self.startRecordingTime)

  def save(self):    
    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(self.recording_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(self.frames))
    wf.close()

  def send(self):
    with open(self.recording_filename, 'rb') as f:
      requests.post(self.upload_route, files={'file': f})

  def stop(self):
    self.stream.stop_stream()
    self.stream.close()
    self.isRecording = False
    
  def done(self):
    self.stop()
    self.save()
    self.send()