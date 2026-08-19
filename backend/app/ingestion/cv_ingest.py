from app.core.logging import configure_logging
from app.ingestion.chunk_indexing import IndexBuilder


class CVIngestCLI:
    """Command-line entry point that rebuilds the CV vector index."""

    def run(self) -> None:
        """Rebuild the vector index and print how many chunks were indexed."""
        configure_logging()
        count = IndexBuilder().rebuild()
        print(f"Indexed {count} chunks.")


def main() -> None:
    """CLI entry point: rebuild the CV vector index."""
    CVIngestCLI().run()


if __name__ == "__main__":
    main()
