import os
import json
import numpy as np
from pathlib import Path

STORE_DIR = Path(__file__).parent / "vector_store"


# ── Save to disk ──────────────────────────────────────
def save_store(chunks: list[str], embeddings: list[list[float]], filename: str):
    name = Path(filename).stem
    store_path = STORE_DIR / f"{name}.json"

    data = {
        "chunks": chunks,
        "embeddings": embeddings
    }

    with open(store_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"[vector_store] Saved {len(chunks)} chunks to {store_path}")


# ── Load from disk ────────────────────────────────────
def load_store(filename: str) -> tuple[list[str], list[list[float]]]:
    name = Path(filename).stem
    store_path = STORE_DIR / f"{name}.json"

    if not store_path.exists():
        raise FileNotFoundError(f"No store found for: {filename}")

    with open(store_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["chunks"], data["embeddings"]


# ── Cosine Similarity ─────────────────────────────────
def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ── Search ────────────────────────────────────────────
def search(query_embedding: list[float], filename: str, top_k: int = 5) -> list[str]:
    chunks, embeddings = load_store(filename)

    scores = [cosine_similarity(query_embedding, emb) for emb in embeddings]
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = [chunks[i] for i in top_indices]
    print(f"[vector_store] Top {top_k} chunks retrieved.")
    return results


# ── List available stores ─────────────────────────────
def list_stores() -> list[str]:
    return [f.stem for f in STORE_DIR.glob("*.json")]