from pathlib import Path
import base64
from openai import OpenAI
from app.config import get_settings, Settings
from app.generation.candidate_generation_prompts import PortraitPromptBuilder
from app.generation.candidate_specifications import CandidateSpecification


class PortraitGenerator:
    """Generates a fictional candidate portrait via the configured image model."""

    def __init__(self, settings: Settings | None = None, client: OpenAI | None = None) -> None:
        """Set up settings and an OpenRouter client, or reuse the ones passed in."""
        self._settings = settings or get_settings()
        self._client = client or OpenAI(
            base_url=self._settings.openrouter_base_url,
            api_key=self._settings.openrouter_api_key,
        )

    def generate(self, candidate: CandidateSpecification, output_path: Path) -> None:
        """Generate a headshot for a candidate and save it to output_path."""

        prompt = PortraitPromptBuilder.build(gender_presentation=candidate.gender, country=candidate.country)

        completion = self._client.chat.completions.create(
            model=self._settings.image_model,
            messages=[{"role": "user", "content": prompt}],
            extra_body={"modalities": ["image", "text"]},
        )

        message = completion.choices[0].message
        images = getattr(message, "images", None) or message.model_dump().get("images")

        if not images:
            raise RuntimeError("Image model did not return an image.")

        image_url = images[0]["image_url"]["url"]
        _, _, image_base64 = image_url.partition("base64,")
        image_bytes = base64.b64decode(image_base64)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_bytes(image_bytes)
