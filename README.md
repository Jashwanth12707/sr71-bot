# SR-71 Blackbird RAG Assistant

A Retrieval-Augmented Generation (RAG) assistant that answers technical, historical, and operational questions about the Lockheed SR-71 Blackbird. The application combines a local document retrieval pipeline using ChromaDB with the Groq API for text generation, wrapped in a FastAPI backend and a responsive glassmorphism web interface.

## Prerequisites

- Python 3.10 or higher
- A Groq API key

## Installation

1. Clone the repository and navigate to the project root:
   ```bash
   git clone <your-repository-url>
   cd sr71-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Database Initialization (Optional)

If the ChromaDB vector database is not already initialized, or if you need to rebuild it from source documents in the `data/` folder:

```bash
python src/rag/vectordb.py
```

## Running the Application

Start the web server using Uvicorn:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Once running, access the web interface in your browser at:
http://127.0.0.1:8000

## Project Architecture

- **`app.py`**: FastAPI server hosting the application backend and serving the static frontend assets.
- **`frontend/`**: The web interface, containing the HTML structural layout, styles, and API request handling.
- **`src/`**: Core logic files.
  - `retriever.py`: Coordinates query embedding generation and similarity searches against ChromaDB.
  - `llm.py`: Constructs prompt contexts and queries the Groq model.
  - `rag/`: Core data ingestion pipelines including document loading, text chunking, and embedding generation.
