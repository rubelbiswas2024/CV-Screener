from app.core.logging import configure_logging
from app.ingestion.chunk_indexing import IndexBuilder


class CVIngest:
    """Command-line entry point that rebuilds the CV vector index."""

    def run(self) -> None:
        """Rebuild the vector index and print how many chunks were indexed."""
        configure_logging()
        count = IndexBuilder().rebuild()
        print(f"Indexed {count} chunks.")

def main() -> None:
    """Entry point: rebuild the CV vector index."""
    CVIngest().run()

if __name__ == "__main__":
    main()
