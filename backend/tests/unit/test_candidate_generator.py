import json
from app.generation.candidate_generator import CandidateGenerator
from app.models.candidate_info import Candidate


def _sample_candidate() -> Candidate:
    return Candidate(
        candidate_id="C001",
        name="Jane Doe",
        headline="Backend Engineer",
        email="jane.doe@example.test",
        phone="+00 000 111 222",
        location="Barcelona, Spain",
        summary="Experienced backend engineer.",
        skills=["Python", "PostgreSQL", "Docker", "Git", "Linux"],
        experience=[
            {
                "company_name": "Acme Corp",
                "role": "Backend Engineer",
                "location": "Barcelona, Spain",
                "start_year": 2019,
                "end_year": None,
                "responsibilities": ["Built APIs", "Owned deployments"],
                "technologies": ["Python", "Docker"],
            }
        ],
        education=[
            {
                "institution": "UPC",
                "degree": "BSc",
                "field": "Computer Science",
                "graduation_year": 2018,
            }
        ],
        languages=["English - C1"],
    )

def test_save_writes_readable_json(tmp_path):
    candidate = _sample_candidate()
    output_path = tmp_path / "candidates" / "C001.json"
    CandidateGenerator.save(candidate, output_path)
    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["candidate_id"] == "C001"
    assert saved["name"] == "Jane Doe"
