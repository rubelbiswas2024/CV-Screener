from pathlib import Path
import pymupdf
from langchain_core.documents import Document


class CVLoader:
    """Loads CV PDFs into LangChain Documents, one per non-empty page."""

    def load_pdf(self, path: Path) -> list[Document]:
        """Turn each non-empty page of a CV PDF into a Document."""

        result = []
        candidate_id = path.stem
        pdf = pymupdf.open(path)

        try:

            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()
                if not text:
                    continue
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                candidate_name = (lines[0] if lines else candidate_id)

                result.append(
                    Document(
                        page_content=text,
                        metadata={"candidate_id": candidate_id, "candidate_name": candidate_name,
                            "source": path.name, "page": page_number},
                    )
                )
        finally:
            pdf.close()

        return result

    def load_directory(self, directory: Path) -> list[Document]:
        """Load every PDF in a directory."""
        documents = []
        for path in sorted(directory.glob("*.pdf")):
            documents.extend(self.load_pdf(path))
        return documents
