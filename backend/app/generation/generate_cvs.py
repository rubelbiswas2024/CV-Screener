import logging
import time
import httpx
from app.config import get_settings
from app.core.logging import configure_logging
from app.generation.candidate_generator import CandidateGenerator
from app.generation.photo_generation import CandidatePhotoGenerator
from app.generation.make_pdf import CandidatePDFRenderer
from app.generation.candidate_specifications import CANDIDATE_SPECS


class CVGenerationPipeline:
    "Generates candidate JSON, photo, and PDF for every candidate specification."

    def __init__(self) -> None:
        "Set up settings, logger, and the generators used for each candidate."
        self._settings = get_settings()
        self._logger = logging.getLogger("generate_cvs")
        self._generator = CandidateGenerator(settings=self._settings)
        self._candidate_photo_generator = CandidatePhotoGenerator(settings=self._settings)
        self._pdf_renderer = CandidatePDFRenderer()

    def run(self) -> None:
        "Generate JSON, photo, and PDF for every candidate spec."

        self._settings.candidate_dir.mkdir(parents=True, exist_ok=True)
        self._settings.image_dir.mkdir(parents=True, exist_ok=True)
        self._settings.cv_dir.mkdir(parents=True, exist_ok=True)

        for index, candidate in enumerate(CANDIDATE_SPECS, start=1):
            self._generate_one(index, candidate)
            time.sleep(0.5)

    def _generate_one(self, index: int, candidate) -> None:
        "Generate one candidate's CV, photo, and PDF; log and move on if it fails."

        candidate_id = (f"C{index:03d}")
        self._logger.info("Generating %s", candidate_id)

        try:
            generated = self._generator.generate(candidate_id=(candidate_id), candidate=candidate)
            json_path = (self._settings.candidate_dir / f"{candidate_id}.json")
            image_path = (self._settings.image_dir / f"{candidate_id}.png")
            pdf_path = (self._settings.cv_dir / f"{candidate_id}.pdf")
            self._generator.save(generated, json_path)

            try:
                self._candidate_photo_generator.generate(candidate=candidate, output_path=image_path)
            except httpx.HTTPStatusError as error:
                self._logger.error(
                    "Skipping photo for %s: Pollinations API returned %s.",
                    candidate_id,
                    error.response.status_code,
                )
            except Exception:
                self._logger.exception("Failed generating photo for %s, continuing without it", candidate_id)

            self._pdf_renderer.render(candidate=generated, image_path=image_path, output_path=pdf_path)

            self._logger.info("Generated %s: %s", candidate_id, generated.name)

        except Exception:

            self._logger.exception("Failed generating %s", candidate_id)


def main() -> None:
    "Eentry point: generate CVs for every candidate spec."
    configure_logging()
    CVGenerationPipeline().run()


if __name__ == "__main__":
    main()
