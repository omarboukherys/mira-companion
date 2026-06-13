"""Text-to-speech generation backed by Groq (PlayAI Dialog)."""

from groq import Groq

from mira.settings import settings


class AudioGenerator:
    """Converts text into spoken audio using Groq's PlayAI TTS model."""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(self, text: str) -> bytes:
        """Generate speech from text and return raw WAV bytes."""
        response = self.client.audio.speech.create(
            model=settings.TTS_MODEL_NAME,
            voice=settings.TTS_VOICE,
            input=text,
            response_format="wav",
        )

        return response.read()


audio_generator = AudioGenerator()