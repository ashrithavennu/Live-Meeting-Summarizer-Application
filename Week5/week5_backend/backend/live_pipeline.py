import sounddevice as sd
import scipy.io.wavfile as wav


def record_live_audio(filename="live_recording.wav", duration=3, fs=16000):
    print("🎙️ Recording...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    wav.write(filename, fs, recording)

    print("✅ Recording saved")

    return filename