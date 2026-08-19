from pydantic import BaseModel, Field


class CandidateExperience(BaseModel):
    """
    Represents a candidate's professional experience, including their role,
    company info, responsibilities, and the technologies used.
    """
    company_name: str
    role: str
    location: str
    start_year: int
    end_year: int | None = None

    responsibilities: list[str] = Field(
        min_length=2,
        max_length=20,
    )

    technologies: list[str] = Field(
        default_factory=list,
    )

class CandidateEducation(BaseModel):
    institution: str
    degree: str
    field: str
    graduation_year: int

class Candidate(BaseModel):
    candidate_id: str
    name: str
    headline: str
    email: str
    phone: str
    location: str
    summary: str

    skills: list[str] = Field(
        min_length=5,
        max_length=15,
    )

    experience: list[CandidateExperience] = Field(
        min_length=1,
        max_length=5,
    )

    education: list[CandidateEducation] = Field(
        min_length=1,
        max_length=3,
    )

    languages: list[str] = Field(
        min_length=1,
        max_length=4,
    )