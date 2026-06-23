'use client'

type TileStatus = 'empty' | 'tbd' | 'correct' | 'present' | 'absent'

interface Props {
  letter?: string
  status?: TileStatus
  position?: number
}

const statusClasses: Record<TileStatus, string> = {
  empty: 'border-2 border-gray-300 dark:border-gray-600',
  tbd: 'border-2 border-gray-500 dark:border-gray-400',
  correct: 'bg-green-500 border-green-500 text-white',
  present: 'bg-yellow-500 border-yellow-500 text-white',
  absent: 'bg-gray-500 border-gray-500 text-white',
}

export default function WordleTile({ letter = '', status = 'empty', position = 0 }: Props) {
  const isRevealed = status !== 'empty' && status !== 'tbd'
  return (
    <div
      className={`
        w-14 h-14 flex items-center justify-center text-2xl font-bold uppercase
        select-none transition-all duration-300
        ${statusClasses[status]}
        ${isRevealed ? 'animate-flip' : ''}
      `}
      style={{ animationDelay: isRevealed ? `${position * 100}ms` : '0ms' }}
    >
      {letter}
    </div>
  )
}
