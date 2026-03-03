import { useState } from "react"

function FileUpload({ onFileReady }) {
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setLoading(true)
    setMessage("")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      })
      const data = await res.json()
      setMessage(`✅ تم رفع الملف — ${data.chunks} chunks`)
      onFileReady(file.name)
    } catch (err) {
      setMessage("❌ حصل خطأ في الرفع")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="file-upload">
      <label className="upload-btn">
        {loading ? "جاري الرفع..." : "📁 ارفع ملف"}
        <input type="file" accept=".pdf,.docx,.txt,.csv,.xlsx" onChange={handleUpload} hidden />
      </label>
      {message && <p className="upload-msg">{message}</p>}
    </div>
  )
}

export default FileUpload