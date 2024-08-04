from pydub import AudioSegment 
import pyaudio

def record_audio(duration):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
   
    stream.stop_stream()
    stream.close()
    p.terminate()


    audio_data = b''.join(frames)
    audio_segment = AudioSegment(data=audio_data, sample_width=2, frame_rate=rate, channels=channels)
    audio_segment.export("recorded_audio.wav", format="wav")

record_audio(5)