'use client'
import WordleTile from './WordleTile'
import type { LetterResult } from '@/types'

interface CompletedRow {
  guess: string
  feedback: LetterResult[]
}

interface Props {
  completedRows: CompletedRow[]
  currentGuess: string
  maxAttempts: number
  wordLength: number
}

export default function WordleBoard({ completedRows, currentGuess, maxAttempts, wordLength }: Props) {
  const rows = Array.from({ length: maxAttempts }, (_, rowIndex) => {
    if (rowIndex < completedRows.length) {
      const { guess, feedback } = completedRows[rowIndex]
      return Array.from({ length: wordLength }, (_, i) => ({
        letter: guess[i] || '',
        status: (feedback[i]?.status ?? 'absent') as 'correct' | 'present' | 'absent',
      }))
    }
    if (rowIndex === completedRows.length) {
      return Array.from({ length: wordLength }, (_, i) => ({
        letter: currentGuess[i] || '',
        status: currentGuess[i] ? 'tbd' : 'empty',
      }))
    }
    return Array.from({ length: wordLength }, () => ({ letter: '', status: 'empty' }))
  })

  return (
    <div className="flex flex-col gap-1">
      {rows.map((row, rowIndex) => (
        <div key={rowIndex} className="flex gap-1">
          {row.map((tile, colIndex) => (
            <WordleTile
              key={colIndex}
              letter={tile.letter}
              status={tile.status as any}
              position={colIndex}
            />
          ))}
        </div>
      ))}
    </div>
  )
}
