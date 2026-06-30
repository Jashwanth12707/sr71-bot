from typing import List

import chromadb

DB_PATH = "chroma_db"
COLLECTION_NAME = "sr71_documents"


def get_collection():
    """
    Returns the ChromaDB collection.
    Creates it if it doesn't already exist.
    """
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def reset_collection():
    """
    Deletes the existing collection and recreates it.
    Useful while rebuilding the vector database.
    """
    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
        print("Existing collection deleted.")
    except Exception:
        print("No existing collection found.")

    client.get_or_create_collection(name=COLLECTION_NAME)

    print("Fresh collection created.")


def add_chunks(
    embedded_chunks: List[dict],
):
    """
    Stores embedded chunks in ChromaDB.
    """

    collection = get_collection()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in embedded_chunks:
        ids.append(chunk["id"])
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])
        metadatas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(ids)} chunks in ChromaDB.")


def search(
    query_embedding,
    top_k: int = 5,
):
    """
    Performs similarity search.
    """

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


if __name__ == "__main__":

    from loaders import load_documents
    from chunker import chunk_documents
    from embeddings import (
        load_model,
        generate_embeddings,
    )

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

    print("Resetting vector database...")
    reset_collection()

    print("Storing embeddings...")
    add_chunks(embedded_chunks)

    print("\nVector database is ready!")