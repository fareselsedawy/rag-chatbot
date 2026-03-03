import { useState } from "react"
import ChatWindow from "./components/ChatWindow"
import "./App.css"

function App() {
  const [activeFile, setActiveFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState("")

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setLoading(true)
    setStatus("processing...")
    const formData = new FormData()
    formData.append("file", file)
    try {
      const res = await fetch("http://127.0.0.1:8000/upload", { method: "POST", body: formData })
      const data = await res.json()
      setStatus(`${data.chunks} chunks`)
      setActiveFile(file.name)
    } catch {
      setStatus("upload failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="header">
        <div className="header-left">
          <div className="logo-dot" />
          <h1>RAG_CHATBOT</h1>
        </div>
        <div className="header-right">
          {status && <span className="upload-status">{status}</span>}
          {activeFile && <span className="file-badge">📄 {activeFile}</span>}
          <label className="upload-btn">
            {loading ? "loading..." : "+ upload file"}
            <input type="file" accept=".pdf,.docx,.txt,.csv,.xlsx" onChange={handleUpload} hidden />
          </label>
        </div>
      </div>

      {activeFile
        ? <ChatWindow filename={activeFile} />
        : (
          <div className="messages">
            <div className="empty-chat">
              <p>Upload a file to start chatting</p>
              <span>PDF · DOCX · TXT · CSV · XLSX</span>
            </div>
          </div>
        )
      }
    </div>
  )
}

export default App