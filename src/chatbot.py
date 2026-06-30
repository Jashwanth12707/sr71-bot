from rag.embeddings import load_model

from retriever import retrieve
from llm import generate_response


def main():

    print("Loading embedding model...")
    model = load_model()

    print("\nSR-71 RAG Chatbot Ready!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        results = retrieve(
            question,
            model,
        )

        answer = generate_response(
            question,
            results,
        )

        print()
        print("Assistant:")
        print(answer)
        print()


if __name__ == "__main__":
    main()