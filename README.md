# 🤖 RAG Chatbot

A full-stack AI-powered chatbot that lets you upload documents and ask questions about them — with voice input/output and PowerPoint generation.

Built from scratch without LangChain or LlamaIndex.

---

## ✨ Features

- 📄 **Multi-format support** — PDF, DOCX, TXT, CSV, XLSX
- 🧠 **RAG pipeline** — Retrieval-Augmented Generation from scratch
- 🎤 **Voice input** — Speak your question (Arabic & English)
- 🔊 **Voice output** — Answers read aloud in the same language
- 📊 **PowerPoint generation** — Ask for a presentation, get a .pptx file
- 📝 **Chat memory** — Remembers last 10 messages per session

---

## 🏗️ Architecture

```
File Upload → Parse → Clean → Chunk → Embed → Store
                                                  ↓
User Question → Embed → Retrieve (top-5) → Agent → LLM → Response
                                                            ↓
                                              Text / PPTX / Voice
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite |
| Backend | FastAPI + Python |
| LLM | Groq (LLaMA 3.1) |
| Embeddings | Google Gemini API |
| Vector Store | NumPy + JSON |
| Voice STT | Web Speech API |
| Voice TTS | SpeechSynthesis API |
| PPTX | python-pptx |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- API keys: Groq, Gemini

### 1. Clone the repo
```bash
git clone https://github.com/fareselsedawy/rag-chatbot.git
cd rag-chatbot
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment variables
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
```

### 4. Run the backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 5. Frontend setup
```bash
cd frontend/rag-ui
npm install
npm run dev
```

### 6. Open the app
```
http://localhost:5173
```

---

## 📁 Project Structure

```
rag-chatbot/
├── backend/
│   ├── main.py           # FastAPI server
│   ├── ingestion.py      # File parsing & chunking
│   ├── embeddings.py     # Gemini embeddings
│   ├── vector_store.py   # NumPy cosine similarity search
│   ├── llm.py            # Groq LLM chat
│   ├── agent.py          # Intent detection & routing
│   ├── pptx_generator.py # PowerPoint generation
│   └── requirements.txt
├── frontend/
│   └── rag-ui/
│       └── src/
│           ├── App.jsx
│           └── components/
│               ├── ChatWindow.jsx
│               └── VoiceButton.jsx
└── .env                  # API keys (not tracked)
```

---

## 💡 How It Works

1. **Upload** a document (PDF, DOCX, TXT, CSV)
2. The pipeline **parses → cleans → chunks** the text
3. Each chunk gets **embedded** via Gemini API and stored
4. You **ask a question** (text or voice)
5. The question gets embedded and compared to stored chunks via **cosine similarity**
6. Top 5 relevant chunks are passed to the **LLM**
7. The **agent** detects your intent: chat / summary / PowerPoint
8. Response is returned as text — or spoken aloud if you used voice

---

## 🔮 Future Improvements

- [ ] Streaming responses (word by word)
- [ ] Multi-file support
- [ ] Persistent chat history (database)
- [ ] Local LLM via Ollama (no rate limits)
- [ ] Better Arabic NLP support
- [ ] Docker deployment

---

## 📬 Contact

**Fares Elsedawy** — [LinkedIn](https://linkedin.com/in/fareselsedawy) · [GitHub](https://github.com/fareselsedawy)
