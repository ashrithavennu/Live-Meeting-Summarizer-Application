import whisper

model = None

def get_model():
    global model
    if model is None:
        print("🔄 Loading Whisper model...")
        model = whisper.load_model("base")   # more stable than tiny
    return model


def transcribe_audio(file_path):
    try:
        model = get_model()

        # ✅ Let Whisper handle audio internally
        result = model.transcribe(file_path)

        return result["text"]

    except Exception as e:
        print("❌ Transcription error:", e)
        return f"❌ Transcription failed: {str(e)}"


# ✅ SUMMARY
import re
from collections import Counter
import heapq

def generate_summary(transcript):
    try:
        if not transcript or "failed" in transcript.lower():
            return "Summary failed ❌"

        # Clean text
        text = re.sub(r'\s+', ' ', transcript)

        # Better sentence splitting
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.split()) > 5]

        if len(sentences) == 0:
            return "Summary not available ❌"

        # Word frequency
        words = re.findall(r'\w+', text.lower())
        freq = Counter(words)

        # Score sentences
        sentence_scores = {}
        for sentence in sentences:
            for word in sentence.lower().split():
                if word in freq:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq[word]

        # Select top sentences
        top_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)

        # Join nicely
        summary = ". ".join(top_sentences)

        return summary + "."

    except Exception as e:
        print("Summary error:", e)
        return f"Summary failed ❌: {str(e)}"


# ✅ MAIN FUNCTION (IMPORTANT)
def process_audio_file(file_path):
    transcript = transcribe_audio(file_path)
    summary = generate_summary(transcript)
    return transcript, summary

from pydub import AudioSegment
import imageio_ffmpeg as ffmpeg

AudioSegment.converter = ffmpeg.get_ffmpeg_exe()

def preprocess_audio(input_path, output_path="processed.wav"):
    audio = AudioSegment.from_file(input_path)

    # Fix format
    audio = audio.set_channels(1)        # mono
    audio = audio.set_frame_rate(16000) # 16kHz

    audio.export(output_path, format="wav")
    return output_path