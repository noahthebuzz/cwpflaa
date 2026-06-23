export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  is_verified: boolean
  is_superadmin: boolean
  created_at: string
}

export interface Puzzle {
  id: string
  puzzle_type: 'wordle' | 'sudoku' | 'crossword'
  date: string
  difficulty: 'easy' | 'medium' | 'hard'
}

export interface LetterResult {
  letter: string
  status: 'correct' | 'present' | 'absent'
}

export interface GuessResult {
  guess: string
  feedback: LetterResult[]
  is_correct: boolean
}

export interface PuzzleSummary {
  id: string
  puzzle_type: 'wordle' | 'sudoku' | 'crossword'
  date: string
  difficulty: 'easy' | 'medium' | 'hard'
  content: Record<string, unknown>
}

export interface WordlePuzzle extends Puzzle {
  content: { word_length: number; max_attempts: number }
}

export interface SudokuPuzzle extends Puzzle {
  content: { grid: number[][]; difficulty: string }
}
