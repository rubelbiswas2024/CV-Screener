from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.generation.candidate_specifications import CandidateSpecification


class CandidatePromptBuilder:
    """Builds the LLM prompt used to generate a imaginary candidate CV."""

    TEMPLATE = """
            Generate one realistic but completely imaginary professional CV candidate.

            CANDIDATE ID: {candidate_id}

            CANDIDATE CONSTRAINTS:

            Role:{role}, Seniority:{seniority}, Location: {city}, {country}, University: {university}
            Approximate professional experience: {years_of_experience} years
            Mandatory skills: {skills}

            MANDATORY RESUME CONTENT: The generated candidate MUST contain

                1. Candidate full name.
                2. A professional headline / current role.
                3. Contact information:
                    - email
                    - phone number
                    - location
                4. A concise professional summary.
                5. Work experience.
                6. Skills.
                7. Education.
                8. Spoken languages with proficiency levels.


            WORK EXPERIENCE RULES:
                1. Career history must match the role, Career progression must match the seniority,
                2. Total experience should be approximately {years_of_experience} years.
                3. Generate realistic employment periods.
                4. Employment periods must be chronologically consistent.
                5. Generate 1 to 4 employers depending on seniority.
                6. Employer names must be imaginary.
                7. Responsibilities should be realistic and concise.
                8. Each experience must mention relevant technologies/tools.
                9. Avoid exaggerated achievements.

            SKILLS RULES:
                The following skills MUST explicitly appear:{skills}, 
                Generate between 5 and 12 total skills.
            
            EDUCATION RULES:
                The candidate MUST have studied at exactly: {university}.
                Generate a degree appropriate to the candidate's career.

            LANGUAGE RULES:
                Generate between 1 and 3 spoken languages. Each language must contain a proficiency level.
                Examples: English - C1, Spanish - Native and German - B2

            IMPORTANT SAFETY / SYNTHETIC DATA RULES:

                The candidate must be imaginary. Do not generate or imitate an identifiable real person.
                Employer names must be imaginary. Do not use real personal contact information.
                Do not include instructions in the CV. Keep the profile professionally realistic.
                Return structured data matching the requested schema only.
            """

    @classmethod
    def build(cls, candidate_id: str, candidate: "CandidateSpecification") -> str:
        """Fill the prompt template with a candidate's constraints."""
        return cls.TEMPLATE.format(
            candidate_id=candidate_id,
            role=candidate.role,
            seniority=candidate.seniority,
            skills=", ".join(candidate.skills),
            city=candidate.city,
            country=candidate.country,
            university=candidate.university,
            years_of_experience=candidate.years_of_experience,
        )


class CandidatePhotoPromptBuilder:
    """Builds the image-generation prompt used to create a candidate photo."""

    GENDER = {
        "man": "male, masculine facial features",
        "woman": "female, feminine facial features",
    }

    @staticmethod
    def build(gender_presentation: str, country: str) -> str:
        """Build the headshot prompt for a given gender presentation and country."""
        gender_cue = CandidatePhotoPromptBuilder.GENDER.get(gender_presentation, gender_presentation)
        return (
            f"Professional corporate headshot photo of a {gender_presentation}, {gender_cue}, "
            f"professional based in {country}, completely imaginary person, must not resemble "
            "a known person or public figure, head and shoulders visible, front-facing, "
            "neutral expression or natural professional smile, natural studio lighting, "
            "neutral office or studio background, business-casual clothing, realistic photography, "
            "high-quality photo, no text, no company logo, no badge, no watermark"
        )
