import pyttsx3
import os
from uuid import uuid4

# 1️⃣ Get all available voices
def get_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return [
        {
            "id": voice.id,
            "name": voice.name,
            "display": f"{voice.name} ({voice.id})"
        }
        for voice in voices
    ]

# 2️⃣ Preview selected voice (short sample)
def preview_voice(voice_id, rate=160):
    sample_text = "This is a sample narration using the selected voice."
    return _synthesize_to_wav(sample_text, voice_id, rate)

# 3️⃣ Generate audio for rewritten text (WAV format)
def generate_audio(text, voice_id, rate=160):
    return _synthesize_to_wav(text, voice_id, rate)

# 🔧 Internal helper: synthesize to WAV and return bytes
def _synthesize_to_wav(text, voice_id, rate):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', rate)

    temp_wav = f"temp_{uuid4().hex}.wav"
    engine.save_to_file(text, temp_wav)
    engine.runAndWait()

    with open(temp_wav, "rb") as f:
        audio_bytes = f.read()

    os.remove(temp_wav)
    return audio_bytes
