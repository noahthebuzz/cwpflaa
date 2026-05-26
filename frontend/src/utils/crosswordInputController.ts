export type CellType = "playable" | "clue" | "block";

export interface GridCell {
  row: number;
  col: number;
  type: CellType;
}

export type GridMatrix = GridCell[][];

export type ArrowDirection = "up" | "down" | "left" | "right";

export interface Position {
  row: number;
  col: number;
}

export interface WordValidationInput {
  answer: string;
  attempts: string[];
}

export interface WordValidationResult {
  isCorrect: boolean;
  countsAsFirstTry: boolean;
  typoTolerated: boolean;
}

const directionVector: Record<ArrowDirection, Position> = {
  up: { row: -1, col: 0 },
  down: { row: 1, col: 0 },
  left: { row: 0, col: -1 },
  right: { row: 0, col: 1 },
};

export function findNextPlayableCell(
  grid: GridMatrix,
  current: Position,
  direction: ArrowDirection,
): Position {
  if (grid.length === 0 || grid[0].length === 0) {
    return current;
  }

  const step = directionVector[direction];
  let next = { row: current.row + step.row, col: current.col + step.col };

  while (next.row >= 0 && next.col >= 0 && next.row < grid.length && next.col < grid[0].length) {
    const cell = grid[next.row][next.col];
    if (cell.type === "playable") {
      return next;
    }
    next = { row: next.row + step.row, col: next.col + step.col };
  }

  return current;
}

function hammingDistance(a: string, b: string): number {
  if (a.length !== b.length) {
    return Number.POSITIVE_INFINITY;
  }

  let distance = 0;
  for (let i = 0; i < a.length; i += 1) {
    if (a[i] !== b[i]) {
      distance += 1;
    }
  }
  return distance;
}

export function validateWordAttempt(input: WordValidationInput): WordValidationResult {
  const normalizedAnswer = input.answer.trim().toUpperCase();
  const attempts = input.attempts.map((attempt) => attempt.trim().toUpperCase());

  if (attempts.length === 0) {
    return { isCorrect: false, countsAsFirstTry: false, typoTolerated: false };
  }

  const finalAttempt = attempts[attempts.length - 1];
  const isCorrect = finalAttempt === normalizedAnswer;

  if (!isCorrect) {
    return { isCorrect: false, countsAsFirstTry: false, typoTolerated: false };
  }

  if (attempts.length === 1) {
    return { isCorrect: true, countsAsFirstTry: true, typoTolerated: false };
  }

  if (attempts.length === 2 && hammingDistance(attempts[0], normalizedAnswer) === 1) {
    return { isCorrect: true, countsAsFirstTry: true, typoTolerated: true };
  }

  return { isCorrect: true, countsAsFirstTry: false, typoTolerated: false };
}
