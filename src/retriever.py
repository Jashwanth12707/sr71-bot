from sentence_transformers import SentenceTransformer

from embeddings import load_model
from vectordb import search


def embed_query(
    question: str,
    model: SentenceTransformer,
) -> list[float]:
    """
    Converts a user question into an embedding vector.
    """

    embedding = model.encode(
        question,
        convert_to_numpy=True,
    )

    return embedding.tolist()


def retrieve(
    question: str,
    model: SentenceTransformer,
    top_k: int = 5,
):
    """
    Retrieves the most relevant chunks for a user question.
    """

    query_embedding = embed_query(
        question,
        model,
    )

    results = search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    return results


if __name__ == "__main__":

    print("Loading embedding model...")
    model = load_model()

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        results = retrieve(
            question,
            model,
        )

        print("\nTop Matching Chunks\n")

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i, (doc, meta, distance) in enumerate(
            zip(documents, metadatas, distances),
            start=1,
        ):
            print("=" * 70)
            print(f"Rank      : {i}")
            print(f"Filename  : {meta['filename']}")
            print(f"Source    : {meta['source']}")
            print(f"Distance  : {distance:.4f}")
            print()
            print(doc[:500])
            print()