"""
PRODIGY INFOTECH INTERNSHIP - TASK 4
Sudoku Solver
Solves Sudoku puzzles using backtracking algorithm
"""

import time
import copy

# ── Display ───────────────────────────────────────────────────────────────────

def print_grid(grid, title=None, original=None):
    if title:
        print(f"\n  {'─'*37}")
        print(f"  {title}")
        print(f"  {'─'*37}")
    print()
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("  ├───────┼───────┼───────┤")
        row_str = "  │ "
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "│ "
            if val == 0:
                row_str += ". "
            else:
                # Highlight solved cells vs original
                if original and original[i][j] == 0 and val != 0:
                    row_str += f"\033[92m{val}\033[0m "  # green for solved
                else:
                    row_str += f"{val} "
        row_str += "│"
        print(row_str)
    print()

# ── Validation ────────────────────────────────────────────────────────────────

def is_valid(grid, row, col, num):
    # Check row
    if num in grid[row]:
        return False
    # Check column
    if num in [grid[r][col] for r in range(9)]:
        return False
    # Check 3×3 box
    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if grid[r][c] == num:
                return False
    return True

def find_empty(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None

# ── Solver ────────────────────────────────────────────────────────────────────

def solve(grid):
    empty = find_empty(grid)
    if not empty:
        return True   # Puzzle solved!
    row, col = empty
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if solve(grid):
                return True
            grid[row][col] = 0  # Backtrack
    return False

def validate_input(grid):
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            if val != 0:
                temp = grid[r][c]
                grid[r][c] = 0
                if not is_valid(grid, r, c, temp):
                    grid[r][c] = temp
                    return False, f"Conflict at row {r+1}, col {c+1}"
                grid[r][c] = temp
    return True, "OK"

# ── Sample Puzzles ────────────────────────────────────────────────────────────

PUZZLES = {
    "Easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    "Medium": [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ],
    "Hard": [
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 4, 0, 7],
        [0, 0, 8, 0, 0, 0, 3, 0, 0],
        [0, 0, 1, 0, 9, 0, 0, 0, 0],
        [3, 0, 0, 4, 0, 0, 2, 0, 0],
        [0, 5, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 6, 0, 0, 0],
    ],
}

def choose_puzzle():
    print("\n  Choose a puzzle:")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard")
    print("  4. Enter custom puzzle")
    while True:
        choice = input("\n  Your choice (1-4): ").strip()
        if choice == '1':
            return copy.deepcopy(PUZZLES["Easy"]), "Easy"
        elif choice == '2':
            return copy.deepcopy(PUZZLES["Medium"]), "Medium"
        elif choice == '3':
            return copy.deepcopy(PUZZLES["Hard"]), "Hard"
        elif choice == '4':
            return enter_custom_puzzle(), "Custom"
        else:
            print("  ❌ Enter 1, 2, 3, or 4.")

def enter_custom_puzzle():
    print("\n  Enter 9 rows of 9 digits (use 0 for empty cells).")
    print("  Example row: 530070000\n")
    grid = []
    for i in range(9):
        while True:
            row_input = input(f"  Row {i+1}: ").strip()
            if len(row_input) == 9 and row_input.isdigit():
                grid.append([int(d) for d in row_input])
                break
            print("  ❌ Enter exactly 9 digits (0-9).")
    return grid

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*44)
    print("   🧩  SUDOKU SOLVER  🧩")
    print("   Prodigy Infotech Internship - Task 4")
    print("="*44)

    while True:
        grid, label = choose_puzzle()
        original = copy.deepcopy(grid)

        print_grid(grid, title=f"  Unsolved Puzzle [{label}]")

        valid, msg = validate_input(grid)
        if not valid:
            print(f"  ❌ Invalid puzzle: {msg}\n")
            continue

        print("  🔄 Solving...")
        start = time.time()
        solved = solve(grid)
        elapsed = time.time() - start

        if solved:
            print_grid(grid, title=f"  ✅ Solved Puzzle [{label}]", original=original)
            print(f"  ⏱️  Solved in {elapsed*1000:.2f} ms\n")
        else:
            print("  ❌ This puzzle has no solution.\n")

        again = input("  Solve another puzzle? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("\n  Thanks for using Sudoku Solver! 👋\n")
            break

if __name__ == "__main__":
    main()
