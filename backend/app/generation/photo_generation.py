import hashlib
from pathlib import Path
from urllib.parse import quote
import httpx
from app.config import get_settings, Settings
from app.generation.candidate_generation_prompts import CandidatePhotoPromptBuilder
from app.generation.candidate_specifications import CandidateSpecification


class CandidatePhotoGenerator:
    """Generates a imaginary candidate photo via the free Pollinations image API."""

    BASE_URL = "https://image.pollinations.ai/prompt"

    def __init__(self, settings: Settings | None = None, client: httpx.Client | None = None) -> None:
        """Set up settings and an HTTP client, or reuse the ones passed in."""
        self._settings = settings or get_settings()
        self._client = client or httpx.Client(timeout=60.0)

    def generate(self, candidate: CandidateSpecification, output_path: Path) -> None:
        """Generate a headshot for a candidate and save it to output_path."""

        prompt = CandidatePhotoPromptBuilder.build(gender_presentation=candidate.gender, country=candidate.country)
        url = f"{self.BASE_URL}/{quote(prompt)}"
        seed = int(hashlib.sha256(output_path.stem.encode()).hexdigest(), 16) % (2**31)

        response = self._client.get(
            url,
            params={
                "width": 512,
                "height": 512,
                "nologo": "true",
                "model": self._settings.image_model,
                "seed": seed,
            },
        )
        response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)
