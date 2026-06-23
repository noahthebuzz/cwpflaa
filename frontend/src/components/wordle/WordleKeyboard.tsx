'use client'
import type { LetterResult } from '@/types'

const ROWS = [
  ['Q','W','E','R','T','Z','U','I','O','P'],
  ['A','S','D','F','G','H','J','K','L'],
  ['ENTER','Y','X','C','V','B','N','M','⌫'],
]

interface Props {
  onKey: (key: string) => void
  letterStates: Record<string, 'correct' | 'present' | 'absent'>
}

const keyClass = (state?: string) => {
  if (state === 'correct') return 'bg-green-500 text-white border-green-500'
  if (state === 'present') return 'bg-yellow-500 text-white border-yellow-500'
  if (state === 'absent') return 'bg-gray-500 text-white border-gray-500'
  return 'bg-gray-200 dark:bg-gray-700 dark:text-white'
}

export default function WordleKeyboard({ onKey, letterStates }: Props) {
  return (
    <div className="flex flex-col gap-1 items-center">
      {ROWS.map((row, i) => (
        <div key={i} className="flex gap-1">
          {row.map(key => (
            <button
              key={key}
              onClick={() => onKey(key)}
              className={`
                h-14 rounded font-bold text-sm uppercase border
                ${key.length > 1 ? 'px-3 text-xs' : 'w-10'}
                ${keyClass(letterStates[key])}
                transition-colors
              `}
            >
              {key}
            </button>
          ))}
        </div>
      ))}
    </div>
  )
}
