export default function Home() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-2">Daily Puzzles</h1>
      <p className="text-gray-500 mb-8">Solve today's puzzles. No account needed.</p>
      <div className="grid gap-4">
        <a href="/wordle" className="block border rounded-xl p-6 hover:bg-gray-50 transition">
          <h2 className="text-2xl font-semibold mb-1">Wordle</h2>
          <p className="text-gray-500">Guess the 5-letter word in 6 tries.</p>
        </a>
        <a href="/sudoku" className="block border rounded-xl p-6 hover:bg-gray-50 transition">
          <h2 className="text-2xl font-semibold mb-1">Sudoku</h2>
          <p className="text-gray-500">Fill the 9x9 grid with digits 1-9.</p>
        </a>
        <a href="/crossword" className="block border rounded-xl p-6 hover:bg-gray-50 transition">
          <h2 className="text-2xl font-semibold mb-1">Schwedenraetsel</h2>
          <p className="text-gray-500">Solve the Swedish-style crossword.</p>
        </a>
      </div>
    </div>
  )
}
