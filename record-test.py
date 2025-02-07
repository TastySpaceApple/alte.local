from audio import AudioRecorder
recorder = AudioRecorder('http://localhost:8000/altar')

recorder.open('test.wav')

try:
  while True:
    recorder.record()
    print(recorder.level)
except KeyboardInterrupt:
  recorder.stop()
  recorder.send()
