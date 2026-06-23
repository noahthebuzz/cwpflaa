'use client'
import { useEffect, useState, useCallback } from 'react'
import WordleBoard from '@/components/wordle/WordleBoard'
import WordleKeyboard from '@/components/wordle/WordleKeyboard'
import type { LetterResult, GuessResult } from '@/types'

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const STORAGE_KEY = (date: string) => `puzzle_progress_${date}_wordle`

interface PuzzleInfo {
  id: string
  content: { word_length: number; max_attempts: number }
  date: string
}

interface CompletedRow {
  guess: string
  feedback: LetterResult[]
}

export default function WordlePage() {
  const [puzzle, setPuzzle] = useState<PuzzleInfo | null>(null)
  const [completedRows, setCompletedRows] = useState<CompletedRow[]>([])
  const [currentGuess, setCurrentGuess] = useState('')
  const [gameStatus, setGameStatus] = useState<'playing' | 'won' | 'lost'>('playing')
  const [message, setMessage] = useState('')
  const [letterStates, setLetterStates] = useState<Record<string, 'correct' | 'present' | 'absent'>>({})

  useEffect(() => {
    fetch(`${API}/api/puzzles/today/wordle`)
      .then(r => r.json())
      .then((data: PuzzleInfo) => {
        setPuzzle(data)
        // restore from localStorage
        const saved = localStorage.getItem(STORAGE_KEY(data.date))
        if (saved) {
          const { guesses, status } = JSON.parse(saved)
          setCompletedRows(guesses || [])
          if (status === 'completed') setGameStatus('won')
          if (status === 'failed') setGameStatus('lost')
          // rebuild letter states
          const states: Record<string, 'correct' | 'present' | 'absent'> = {}
          for (const row of (guesses || [])) {
            for (const fb of row.feedback) {
              const cur = states[fb.letter]
              if (cur !== 'correct') states[fb.letter] = fb.status
            }
          }
          setLetterStates(states)
        }
      })
      .catch(() => setMessage('No Wordle puzzle available today.'))
  }, [])

  const showMessage = (msg: string) => {
    setMessage(msg)
    setTimeout(() => setMessage(''), 2500)
  }

  const submitGuess = useCallback(async () => {
    if (!puzzle || currentGuess.length !== puzzle.content.word_length) {
      showMessage(`Word must be ${puzzle?.content.word_length} letters`)
      return
    }
    const token = localStorage.getItem('access_token')
    const res = await fetch(`${API}/api/puzzles/${puzzle.id}/wordle/guess`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      credentials: 'include',
      body: JSON.stringify({ guess: currentGuess }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      showMessage(err.detail || 'Error submitting guess')
      return
    }
    const data: GuessResult = await res.json()
    const newRows = [...completedRows, { guess: data.guess, feedback: data.feedback }]
    setCompletedRows(newRows)
    setCurrentGuess('')

    // update letter states
    setLetterStates(prev => {
      const next = { ...prev }
      for (const fb of data.feedback) {
        if (next[fb.letter] !== 'correct') next[fb.letter] = fb.status
      }
      return next
    })

    let newStatus: 'playing' | 'won' | 'lost' = 'playing'
    if (data.is_correct) {
      setGameStatus('won')
      newStatus = 'won'
      showMessage('Excellent! 🎉')
    } else if (newRows.length >= puzzle.content.max_attempts) {
      setGameStatus('lost')
      newStatus = 'lost'
      showMessage('Game over!')
    }

    // persist to localStorage
    localStorage.setItem(STORAGE_KEY(puzzle.date), JSON.stringify({
      guesses: newRows,
      status: newStatus === 'won' ? 'completed' : newStatus === 'lost' ? 'failed' : 'pending',
    }))
  }, [puzzle, currentGuess, completedRows])

  const handleKey = useCallback((key: string) => {
    if (gameStatus !== 'playing' || !puzzle) return
    if (key === 'ENTER') { submitGuess(); return }
    if (key === '⌫' || key === 'BACKSPACE') {
      setCurrentGuess(g => g.slice(0, -1)); return
    }
    if (/^[A-ZÜÖÄ]$/.test(key) && currentGuess.length < puzzle.content.word_length) {
      setCurrentGuess(g => g + key)
    }
  }, [gameStatus, puzzle, currentGuess, submitGuess])

  useEffect(() => {
    const handler = (e: KeyboardEvent) => handleKey(e.key.toUpperCase())
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [handleKey])

  if (!puzzle && !message) {
    return <div className="flex items-center justify-center h-64 text-gray-500">Loading…</div>
  }

  return (
    <div className="flex flex-col items-center gap-6 py-8 px-4">
      <h1 className="text-3xl font-bold">Wordle</h1>

      {message && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 bg-black text-white px-4 py-2 rounded-lg text-sm font-semibold z-50">
          {message}
        </div>
      )}

      {puzzle ? (
        <>
          {gameStatus === 'won' && (
            <div className="text-green-600 font-bold text-lg">You won! 🎉</div>
          )}
          {gameStatus === 'lost' && (
            <div className="text-red-500 font-bold text-lg">Better luck tomorrow!</div>
          )}
          <WordleBoard
            completedRows={completedRows}
            currentGuess={currentGuess}
            maxAttempts={puzzle.content.max_attempts}
            wordLength={puzzle.content.word_length}
          />
          <WordleKeyboard onKey={handleKey} letterStates={letterStates} />
        </>
      ) : (
        <p className="text-gray-500">{message}</p>
      )}
    </div>
  )
}
