import os
import asyncio
from contextlib import asynccontextmanager
from typing import List

import numpy as np
import faiss
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
DATA_FILE = "DATA.txt"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
GROQ_MODEL = "llama-3.1-8b-instant"

# --- GLOBAL STORAGE ---
# We store the heavy AI models here so they persist
app_state = {
    "text_chunks": [],
    "index": None,
    "model": None,
    "groq_client": None
}

# --- DATA VALIDATION (Pydantic) ---
# This ensures users send the correct data format
class AskRequest(BaseModel):
    message: str

class AskResponse(BaseModel):
    query: str
    reply: str
    top_chunks: List[str]

# --- HELPER FUNCTIONS ---
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def initialize_system():
    """Run this ONCE when server starts"""
    print("--- SYSTEM STARTUP: Loading Models ---")
    
    # Initialize Clients
    app_state["model"] = SentenceTransformer(EMBEDDING_MODEL)
    app_state["groq_client"] = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Initialize Index
    app_state["index"] = faiss.IndexFlatL2(EMBEDDING_DIM)

    # Auto-load Data if file exists
    if os.path.exists(DATA_FILE):
        print(f"Found {DATA_FILE}, processing...")
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_text = f.read()
        
        chunks = chunk_text(raw_text)
        app_state["text_chunks"] = chunks
        
        if chunks:
            embeddings = app_state["model"].encode(chunks, convert_to_numpy=True)
            embeddings = np.array(embeddings).astype("float32")
            app_state["index"].add(embeddings)
            
        print(f"--- SUCCESS: Loaded {len(chunks)} chunks ---")
    else:
        print(f"--- WARNING: {DATA_FILE} not found. Upload it to Hugging Face Files. ---")

# --- LIFESPAN MANAGER ---
# This is the modern way to handle startup/shutdown in FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_system()
    yield
    print("Shutting down...")

# --- APP SETUP ---
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Simple check to see if server is running"""
    return {
        "status": "online", 
        "chunks_loaded": len(app_state["text_chunks"])
    }

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    # Unpack globals
    index = app_state["index"]
    chunks = app_state["text_chunks"]
    model = app_state["model"]
    groq = app_state["groq_client"]

    # Safety Check
    if not chunks or index.ntotal == 0:
        return AskResponse(
            query=req.message, 
            reply="System is not ready. Please ensure DATA.txt is uploaded.", 
            top_chunks=[]
        )

    # 1. EMBEDDING (Heavy CPU Task)
    # We run this in a thread so it doesn't block other users
    query_emb = await asyncio.to_thread(model.encode, [req.message], convert_to_numpy=True)
    query_emb = np.array(query_emb).astype("float32")

    # 2. SEARCH (Fast)
    D, I = index.search(query_emb, k=3)
    
    # Filter valid results
    valid_indices = [i for i in I[0] if i >= 0 and i < len(chunks)]
    if not valid_indices:
        return AskResponse(query=req.message, reply="No relevant context found in the data.", top_chunks=[])
    
    results = [chunks[i] for i in valid_indices]

    # 3. GENERATION (Network Wait)
    context_str = "\n".join(results)
    prompt = f"Context:\n{context_str}\n\nUser Question: {req.message}\n\nAnswer clearly based on the context above."

    try:
        # Run Groq in a thread to keep the server responsive
        chat_completion = await asyncio.to_thread(
            groq.chat.completions.create,
            messages=[{"role": "user", "content": prompt}],
            model=GROQ_MODEL
        )
        reply = chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Groq API Error: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI provider.")

    return AskResponse(
        query=req.message,
        reply=reply,
        top_chunks=results
    )

# Local Development Entry Point
if __name__ == "__main__":
    import uvicorn
    # This block is ignored by Docker if you use the correct CMD
    uvicorn.run(app, host="0.0.0.0", port=8080)