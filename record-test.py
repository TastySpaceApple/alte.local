from audio_recorder import AudioRecorder 
recorder = AudioRecorder('http://atra-bce32f116e3f.herokuapp.com/alte')

recorder.open('test.wav')

try:
  while True:
    recorder.record()
    print(recorder.level)
except KeyboardInterrupt:
  recorder.stop()
  recorder.save()
  recorder.send()
  print("sent")
