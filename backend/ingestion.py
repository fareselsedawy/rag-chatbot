import os
import re
import unicodedata
from pathlib import Path

import fitz  # pymupdf
import docx
import pandas as pd


# ── Constants ────────────────────────────────────────
UPLOAD_DIR = Path(__file__).parent / "uploads"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


# ── 1. Parse File ─────────────────────────────────────
def parse_file(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return _parse_pdf(file_path)
    elif ext == ".docx":
        return _parse_docx(file_path)
    elif ext == ".txt":
        return _parse_txt(file_path)
    elif ext in [".csv", ".xlsx"]:
        return _parse_table(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _parse_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def _parse_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def _parse_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        return f.read()


def _parse_table(path: str) -> str:
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    return df.to_string(index=False)


# ── 2. Clean Text ─────────────────────────────────────
def clean_text(text: str) -> str:
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)
    # Remove extra whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    # Remove special chars but keep Arabic, English, numbers, punctuation
    text = re.sub(r"[^\w\s\u0600-\u06FF.,!?;:()\-]", "", text)
    return text.strip()


# ── 3. Chunk Text ─────────────────────────────────────
def chunk_text(text: str) -> list[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# ── 4. Main Pipeline ──────────────────────────────────
def process_file(file_path: str) -> list[str]:
    print(f"[ingestion] Parsing: {file_path}")
    raw_text = parse_file(file_path)

    print(f"[ingestion] Cleaning...")
    clean = clean_text(raw_text)

    print(f"[ingestion] Chunking...")
    chunks = chunk_text(clean)

    print(f"[ingestion] Done — {len(chunks)} chunks created.")
    return chunks