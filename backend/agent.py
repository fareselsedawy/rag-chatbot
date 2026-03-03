import os
from llm import chat
from embeddings import embed_query
from vector_store import search


# ── Detect intent ─────────────────────────────────────
def detect_intent(question: str) -> str:
    question_lower = question.lower()

    pptx_keywords = ["powerpoint", "pptx", "presentation", "slides", "باور بوينت", "بوربوينت", "سلايد", "عرض", "باور", "بوينت"]
    summary_keywords = ["summary", "summarize", "ملخص", "لخص", "خلاصة"]

    for kw in pptx_keywords:
        if kw in question_lower:
            return "pptx"

    for kw in summary_keywords:
        if kw in question_lower:
            return "summary"

    return "chat"


# ── Main agent ────────────────────────────────────────
def run_agent(
    question: str,
    filename: str,
    history: list[dict] = []
) -> dict:

    # 1. Embed the question
    query_emb = embed_query(question)

    # 2. Retrieve relevant chunks
    chunks = search(query_emb, filename, top_k=5)

    # 3. Detect intent
    intent = detect_intent(question)

    # 4. Execute based on intent
    if intent == "pptx":
        from pptx_generator import generate_pptx
        answer = "جاري إنشاء ملف PowerPoint..."
        pptx_path = generate_pptx(question, chunks)
        return {
            "intent": "pptx",
            "answer": answer,
            "file": pptx_path
        }

    elif intent == "summary":
        summary_question = "Please provide a comprehensive summary of the document."
        answer = chat(summary_question, chunks, history)
        return {
            "intent": "summary",
            "answer": answer,
            "file": None
        }

    else:
        answer = chat(question, chunks, history)
        return {
            "intent": "chat",
            "answer": answer,
            "file": None
        }