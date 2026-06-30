"""
SR-71 Blackbird AI — FastAPI Backend
=====================================
Wraps the existing RAG pipeline with a web API.
The embedding model is loaded once at startup.
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Ensure the `src/` directory is on sys.path so that existing imports
# (retriever, llm, rag.*) resolve correctly — without modifying those files.
# ---------------------------------------------------------------------------
SRC_DIR = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC_DIR))

from rag.embeddings import load_model          # noqa: E402
from retriever import retrieve                 # noqa: E402
from llm import generate_response              # noqa: E402

# ---------------------------------------------------------------------------
# Application state — populated once during the lifespan startup event.
# ---------------------------------------------------------------------------
embedding_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the embedding model once when the server starts."""
    global embedding_model
    print("[*] Loading embedding model...")
    embedding_model = load_model()
    print("[OK] Embedding model loaded - server is ready.")
    yield
    # Shutdown: nothing to clean up.


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SR-71 Blackbird AI",
    description="Ask anything about the world's fastest reconnaissance aircraft.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow every origin during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    """
    Receive a question, run retrieval + generation, return the answer.
    """
    results = retrieve(payload.question, embedding_model)
    answer = generate_response(payload.question, results)
    return ChatResponse(answer=answer)


# ---------------------------------------------------------------------------
# Serve the frontend
# ---------------------------------------------------------------------------
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"

# Mount static assets (CSS, JS, images) under /static
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
async def serve_frontend():
    """Return the main HTML page."""
    return FileResponse(str(FRONTEND_DIR / "index.html"))
