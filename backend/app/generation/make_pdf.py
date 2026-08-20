from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from app.models.candidate_info import Candidate


class CandidatePDFRenderer:
    """Renders a candidate's structured CV data into a formatted PDF resume."""

    def _build_styles(self):
        """Add the section/body/meta paragraph styles used by the CV layout."""
        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="CVSection",
                parent=styles["Heading2"],
                fontSize=11,
                leading=14,
                spaceBefore=10,
                spaceAfter=5,
            )
        )

        styles.add(
            ParagraphStyle(
                name="CVBody",
                parent=styles["BodyText"],
                fontSize=9,
                leading=12,
            )
        )

        styles.add(
            ParagraphStyle(
                name="CVMeta",
                parent=styles["BodyText"],
                fontSize=8,
                leading=10,
                textColor=colors.HexColor(
                    "#666666"
                ),
            )
        )

        return styles

    def render(self, candidate: Candidate, image_path: Path, output_path: Path) -> None:
        """Build the CV PDF and write it to output_path."""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        styles = self._build_styles()

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=16 * mm,
            rightMargin=16 * mm,
            topMargin=14 * mm,
            bottomMargin=14 * mm,
            title=f"{candidate.name} CV",
        )

        identity = Paragraph(
            (
                f"<font size='17'>"
                f"<b>{candidate.name}</b>"
                f"</font>"
                f"<br/>"
                f"{candidate.headline}"
                f"<br/><br/>"
                f"{candidate.location}"
                f"<br/>"
                f"{candidate.email}"
                f"<br/>"
                f"{candidate.phone}"
            ),
            styles["CVBody"],
        )

        if image_path.exists():
            candidate_photo = Image(
                str(image_path),
                width=32 * mm,
                height=32 * mm,
            )

            header = Table(
                [[candidate_photo, identity]],
                colWidths=[
                    38 * mm,
                    128 * mm,
                ],
            )
        else:
            header = Table(
                [[identity]],
                colWidths=[166 * mm],
            )

        header.setStyle(
            TableStyle(
                [
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        0,
                    ),
                ]
            )
        )

        story = [
            header, Spacer(1, 8),

            Paragraph(
                "PROFILE", styles["CVSection"],
            ),

            Paragraph(
                candidate.summary, styles["CVBody"],
            ),

            Paragraph(
                "SKILLS",styles["CVSection"],
            ),

            Paragraph(
                " · ".join(
                    candidate.skills
                ), styles["CVBody"]),

            Paragraph("WORK EXPERIENCE", styles["CVSection"]),
        ]

        for experience in (candidate.experience):

            end_year = (
                str(experience.end_year)
                if experience.end_year
                else "Present"
            )

            block = [
                Paragraph(
                    (
                        f"<b>{experience.role}</b>"
                        f" — "
                        f"{experience.company_name}"
                    ),
                    styles["CVBody"],
                ),

                Paragraph(
                    (
                        f"{experience.location}"
                        f" | "
                        f"{experience.start_year}"
                        f"-{end_year}"
                    ),
                    styles["CVMeta"],
                ),
            ]

            for responsibility in (experience.responsibilities):
                block.append(Paragraph(f"# {responsibility}", styles["CVBody"]))

            block.append(
                Paragraph(
                    (
                        "<b>Technologies:</b> "
                        + ", ".join(
                            experience.technologies
                        )
                    ),
                    styles["CVMeta"],
                )
            )

            block.append(Spacer(1, 7))

            story.append(KeepTogether(block))

        story.append(Paragraph("EDUCATION", styles["CVSection"]))

        for education in (candidate.education):
            story.append(
                Paragraph(
                    (
                        f"<b>{education.degree}"
                        f" in {education.field}</b>"
                        f"<br/>"
                        f"{education.institution}"
                        f" — "
                        f"{education.graduation_year}"
                    ),
                    styles["CVBody"],
                )
            )

            story.append(Spacer(1, 5))

        story.append(Paragraph("LANGUAGES", styles["CVSection"]))

        story.append(Paragraph(" · ".join(candidate.languages), styles["CVBody"]))
        document.build(story)
