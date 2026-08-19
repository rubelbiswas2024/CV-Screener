from app.RAG.graph import graph


class ChatSession:
    """Interactive command-line chat loop over the RAG pipeline."""

    def __init__(self) -> None:
        """Use the shared RAG pipeline instance."""
        self._pipeline = graph

    def run(self) -> None:
        """Ask questions in a loop and print answers with sources until the user quits."""
        while True:
            question = input("\nQuestion: ").strip()

            if question.lower() in {"exit", "quit"}:
                break

            result = self._pipeline.invoke({"question": question})

            print("\nAnswer:")
            print(result["answer"])
            print("\nSources:")

            for source in result.get("sources", []):
                print(
                    (
                        f"- "
                        f"{source['candidate_name']}"
                        f" | "
                        f"{source['file']}"
                        f" | "
                        f"page "
                        f"{source['page']}"
                    )
                )


def main() -> None:
    """CLI entry point: start the interactive chat session."""
    ChatSession().run()


if __name__ == "__main__":
    main()
