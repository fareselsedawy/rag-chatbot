import { useState, useRef, useEffect } from "react"
import VoiceButton from "./VoiceButton"

function ChatWindow({ filename }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [speaking, setSpeaking] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const stopSpeaking = () => {
    window.speechSynthesis.cancel()
    setSpeaking(false)
  }

  const sendMessage = async (text, isVoice = false) => {
    const question = text || input
    if (!question.trim()) return
    setInput("")
    setMessages(prev => [...prev, { role: "user", content: question }])
    setLoading(true)

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, filename }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setMessages(prev => [...prev, { role: "assistant", content: data.answer, intent: data.intent, file: data.file }])

      if (data.answer && isVoice) {
        const isArabic = /[\u0600-\u06FF]/.test(data.answer)
        const utterance = new SpeechSynthesisUtterance(data.answer)
        utterance.lang = isArabic ? "ar-EG" : "en-US"
        utterance.onstart = () => setSpeaking(true)
        utterance.onend = () => setSpeaking(false)
        window.speechSynthesis.cancel()
        window.speechSynthesis.speak(utterance)
      }

      if (data.intent === "pptx" && data.file) {
            const fname = data.file.split(/[\\/]/).pop()
            window.location.href = `http://127.0.0.1:8000/download/${fname}`
        }
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", content: `Error: ${err.message}` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="messages">
        {messages.length === 0 && (
          <div className="empty-chat">
            <p>Ask anything about the document</p>
            <span>or request a PowerPoint / summary</span>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <span className="msg-label">{msg.role === "user" ? "you" : "assistant"}</span>
            <div className="msg-bubble">{msg.content}</div>
            {msg.intent === "pptx" && <span className="badge">📊 PowerPoint generated</span>}
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <span className="msg-label">assistant</span>
            <div className="typing">
              <span /><span /><span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="input-area">
        <div className="input-row">
          <VoiceButton onResult={sendMessage} />
          {speaking && (
            <button className="voice-btn" onClick={stopSpeaking} title="Stop">⏹</button>
          )}
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && sendMessage()}
            placeholder="Ask a question..."
          />
          <button className="send-btn" onClick={() => sendMessage()}>Send</button>
        </div>
        <p className="input-hint">press Enter to send · click 🎤 to speak</p>
      </div>
    </>
  )
}

export default ChatWindow