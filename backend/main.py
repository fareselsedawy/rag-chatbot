import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import traceback

load_dotenv(r"H:\rag-chatbot\.env")

from ingestion import process_file
from embeddings import embed_chunks
from vector_store import save_store, list_stores
from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
chat_histories: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    question: str
    filename: str


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    chunks = process_file(str(file_path))
    embeddings = embed_chunks(chunks)
    save_store(chunks, embeddings, file.filename)
    return {"message": "File processed successfully", "filename": file.filename, "chunks": len(chunks)}


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        history = chat_histories.get(req.filename, [])
        result = run_agent(req.question, req.filename, history)
        history.append({"role": "user", "content": req.question})
        history.append({"role": "assistant", "content": result["answer"]})
        chat_histories[req.filename] = history[-10:]
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files")
async def get_files():
    return {"files": list_stores()}


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(file_path), filename=filename)


@app.get("/")
async def root():
    return {"status": "RAG Chatbot API is running"}