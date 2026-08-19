import { useState } from 'react'

const API_URL = 'http://localhost:8000/api/chat'

function App() {
  const [question, setQuestion] = useState('')
  const [askedQuestion, setAskedQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const askQuestion = async () => {
    const submittedQuestion = question.trim()
    if (!submittedQuestion || loading) return

    setLoading(true)
    setError('')
    setAskedQuestion(submittedQuestion)
    setAnswer('')
    setQuestion('')

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: submittedQuestion }),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setAnswer(data.answer)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      askQuestion()
    }
  }

  return (
    <div className="container">
      <h1>CV Screener Chat</h1>

      <div className="response-box">
        <h2>Response</h2>

        {askedQuestion && <p className="asked-question">Q: {askedQuestion}</p>}

        <textarea
          className="response-text"
          value={loading ? 'Asking...' : answer}
          readOnly
          rows={14}
          placeholder="The answer will appear here."
        />
      </div>

      {error && <p className="error">{error}</p>}

      <div className="query-box">
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the CV collection..."
          rows={3}
        />
        <button onClick={askQuestion} disabled={loading}>
          {loading ? 'Asking...' : 'Ask'}
        </button>
      </div>
    </div>
  )
}

export default App
