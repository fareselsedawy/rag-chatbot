import { useState } from "react"

function VoiceButton({ onResult }) {
  const [listening, setListening] = useState(false)

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      alert("Use Chrome for voice support")
      return
    }

    const recognition = new SpeechRecognition()
    recognition.lang = "en-US"
    recognition.interimResults = false

    recognition.onstart = () => setListening(true)
    recognition.onend = () => setListening(false)
    recognition.onerror = () => setListening(false)

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript
      onResult(transcript, true)
    }

    recognition.start()
  }

  return (
    <button
      className={`voice-btn ${listening ? "listening" : ""}`}
      onClick={startListening}
      title="Speak"
    >
      {listening ? "🔴" : "🎤"}
    </button>
  )
}

export default VoiceButton