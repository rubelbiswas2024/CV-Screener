from __future__ import annotations
import random
from pathlib import Path
import anthropic
from app.config import get_settings, Settings
from app.generation.candidate_generation_prompts import CandidatePromptBuilder
from app.generation.candidate_specifications import CandidateSpecification
from app.models.candidate_info import Candidate


class CandidateGenerator:
    """Generates a fictional, structured candidate CV via the configured LLM."""

    def __init__(self, settings: Settings | None = None, client: anthropic.Anthropic | None = None) -> None:
        """Set up settings and an Anthropic client, or reuse the ones passed in."""
        self._settings = settings or get_settings()
        self._client = client or anthropic.Anthropic(api_key=self._settings.anthropic_api_key)

    def generate(self, candidate_id: str, candidate: CandidateSpecification) -> Candidate:
        """Ask the LLM for a fictional CV, then patch in the fields that must be exact."""

        location = (f"{candidate.city}, "f"{candidate.country}")

        prompt = CandidatePromptBuilder.build(candidate_id=candidate_id, candidate=candidate)

        response = self._client.messages.parse(
            model=self._settings.llm_model,
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}],
            output_format=Candidate,
        )

        generated = response.parsed_output

        # Deterministic assignment fields.
        generated.candidate_id = (candidate_id)
        generated.location = (location)
        number = random.randint(100, 999)

        generated.email = (f"{candidate_id.lower()}." f"{number}" "@example.test")

        generated.phone = (f"+00 000 " f"{random.randint(100, 999)} " f"{random.randint(100, 999)}")

        # Guarantee required skills.
        existing_lower = {skill.lower() for skill in generated.skills}

        for skill in (candidate.skills):

            if (
                skill.lower()
                not in existing_lower
            ):

                generated.skills.append(skill)

                existing_lower.add(skill.lower())

        # Guarantee university.
        if generated.education:
            generated.education[0].institution = (candidate.university)

        return generated

    @staticmethod
    def save(candidate: Candidate, output_path: Path) -> None:
        """Write a candidate to disk as JSON."""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(candidate.model_dump_json(indent=2), encoding="utf-8")
