import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(r"H:\rag-chatbot\.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


def chat(question: str, context_chunks: list[str], history: list[dict] = []) -> str:
    context = "\n\n".join(context_chunks)

    system_prompt = f"""You are a helpful assistant that answers questions based on the provided document context.
Always answer based on the context below. If the answer is not in the context, say "I don't have enough information in the provided documents."
Answer in the same language the user is using.

Context:
{context}"""

    messages = [{"role": "system", "content": system_prompt}]
    messages += history
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=1024
    )

    return response.choices[0].message.content


def ask(question: str, context_chunks: list[str]) -> str:
    return chat(question, context_chunks, history=[])