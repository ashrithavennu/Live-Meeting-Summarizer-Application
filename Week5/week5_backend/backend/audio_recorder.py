import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

fs = 16000  # sample rate
recording = []
is_recording = False


def start_recording():
    global recording, is_recording
    recording = []
    is_recording = True

    def callback(indata, frames, time, status):
        if is_recording:
            recording.append(indata.copy())

    sd.InputStream(callback=callback, channels=1, samplerate=fs).start()


def stop_recording(filename="live_audio.wav"):
    global is_recording
    is_recording = False

    audio = np.concatenate(recording, axis=0)
    wav.write(filename, fs, audio)

    return filename