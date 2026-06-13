"""Image generation backed by Together AI (FLUX)."""

import base64

from together import Together

from mira.settings import settings


class ImageGenerator:
    """Generates images from text prompts using Together AI's FLUX model."""

    def __init__(self):
        self.client = Together(api_key=settings.TOGETHER_API_KEY)

    def generate(self, prompt: str) -> bytes:
        """Generate an image from a text prompt and return raw PNG bytes."""
        response = self.client.images.generate(
            prompt=prompt,
            model=settings.IMAGE_MODEL_NAME,
            width=1024,
            height=768,
            steps=4,
            n=1,
            response_format="b64_json",
        )

        b64_image = response.data[0].b64_json
        return base64.b64decode(b64_image)


image_generator = ImageGenerator()