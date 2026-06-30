from typing import List

from sentence_transformers import SentenceTransformer

from models import Chunk


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_model() -> SentenceTransformer:
    """
    Load and return the embedding model.
    """
    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(
    chunks: List[Chunk],
    model: SentenceTransformer,
) -> list[dict]:
    """
    Generate embeddings for all chunks.

    Returns:
        [
            {
                "id": ...,
                "text": ...,
                "embedding": [...],
                "metadata": {...}
            },
            ...
        ]
    """

    texts = [chunk.text for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):

        embedded_chunks.append(
            {
                "id": chunk.id,
                "text": chunk.text,
                "embedding": embedding.tolist(),
                "metadata": chunk.metadata,
            }
        )

    return embedded_chunks


if __name__ == "__main__":

    from loaders import load_documents
    from chunker import chunk_documents

    print("Loading documents...")
    documents = load_documents()

    print("Chunking documents...")
    chunks = chunk_documents(documents)

    print("Loading embedding model...")
    model = load_model()

    print("Generating embeddings...")
    embedded_chunks = generate_embeddings(
        chunks,
        model,
    )

    print(f"\nTotal Chunks: {len(embedded_chunks)}")

    print("\nFirst Embedded Chunk:\n")

    print(f"ID: {embedded_chunks[0]['id']}")
    print(f"Embedding Dimensions: {len(embedded_chunks[0]['embedding'])}")
    print(f"Metadata: {embedded_chunks[0]['metadata']}")  