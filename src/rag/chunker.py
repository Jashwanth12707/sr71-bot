from typing import List

from models import Chunk


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunk(
    document: dict,
    chunk_text: str,
    chunk_number: int,
    total_chunks: int,
) -> Chunk:

    return Chunk(
        id=f"{document['filename']}_chunk_{chunk_number}",
        text=chunk_text,
        metadata={
            "filename": document["filename"],
            "source": document["source"],
            "path": document["path"],
            "extension": document["extension"],
            "chunk_number": chunk_number,
            "total_chunks": total_chunks,
        },
    )


def chunk_document(
    document: dict,
) -> List[Chunk]:

    text_chunks = split_text(document["text"])

    document_chunks = []

    total_chunks = len(text_chunks)

    for chunk_number, chunk_text in enumerate(text_chunks):

        chunk = create_chunk(
            document=document,
            chunk_text=chunk_text,
            chunk_number=chunk_number,
            total_chunks=total_chunks,
        )

        document_chunks.append(chunk)

    return document_chunks


def chunk_documents(
    documents: list[dict],
) -> List[Chunk]:

    all_chunks = []

    for document in documents:

        document_chunks = chunk_document(document)

        all_chunks.extend(document_chunks)

    return all_chunks


if __name__ == "__main__":

    from loaders import load_documents

    documents = load_documents()

    chunks = chunk_documents(documents)

    print(f"Documents : {len(documents)}")
    print(f"Chunks    : {len(chunks)}")

    print()

    print(chunks[0])