from dataclasses import dataclass

@dataclass
class ChunkMetadata:
    filename: str
    source: str
    path: str
    extension: str
    chunk_number: int
    total_chunks: int

@dataclass
class Chunk:
    id:str
    text:str
    metadata:ChunkMetadata