import os
from dotenv import load_dotenv
from google import genai

load_dotenv(r"H:\rag-chatbot\.env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "gemini-embedding-001"


# ── Embed single text ─────────────────────────────────
def embed_text(text: str) -> list[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )
    return result.embeddings[0].values


# ── Embed list of chunks ──────────────────────────────
def embed_chunks(chunks: list[str]) -> list[list[float]]:
    embeddings = []
    for i, chunk in enumerate(chunks):
        print(f"[embeddings] Embedding chunk {i+1}/{len(chunks)}...")
        emb = embed_text(chunk)
        embeddings.append(emb)
    return embeddings


# ── Embed a query ─────────────────────────────────────
def embed_query(query: str) -> list[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query
    )
    return result.embeddings[0].values