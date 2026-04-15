# ============================================================
#  Topic 5: Recursion & Backtracking
#  Covers: base cases, recursion tree, memoization,
#          N-Queens, maze solver, subsets, permutations
# ============================================================

import sys
sys.setrecursionlimit(10000)

# ────────────────────────────────────────────────────────────
#  RECURSION BASICS
# ────────────────────────────────────────────────────────────

print("=" * 55)
print("  RECURSION BASICS")
print("=" * 55)

# 1. Factorial
def factorial(n):
    if n <= 1: return 1             # base case
    return n * factorial(n - 1)    # recursive case

print("\n1. Factorial")
for i in range(8): print(f"   {i}! = {factorial(i)}")


# 2. Fibonacci — naive O(2^n)
def fib_naive(n):
    if n <= 1: return n
    return fib_naive(n-1) + fib_naive(n-2)

# Fibonacci — memoized O(n)
def fib_memo(n, memo={}):
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

print("\n2. Fibonacci (memoized)")
print("   First 15:", [fib_memo(i) for i in range(15)])


# 3. Sum of digits
def sum_of_digits(n):
    if n == 0: return 0
    return n % 10 + sum_of_digits(n // 10)

print("\n3. Sum of digits")
for n in [0, 5, 123, 9876]:
    print(f"   sum_digits({n}) = {sum_of_digits(n)}")


# 4. Power — O(log n) via fast exponentiation
def power(base, exp):
    if exp == 0: return 1
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    return base * power(base, exp - 1)

print("\n4. Fast Power")
print(f"   2^10 = {power(2, 10)}")
print(f"   3^5  = {power(3, 5)}")


# 5. Binary search (recursive)
def bin_search(arr, target, lo=0, hi=None):
    if hi is None: hi = len(arr) - 1
    if lo > hi: return -1
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    if arr[mid] < target:  return bin_search(arr, target, mid+1, hi)
    return bin_search(arr, target, lo, mid-1)

arr = [1,3,5,7,9,11,13]
print("\n5. Binary Search (recursive)")
print(f"   Search 7 in {arr}: index {bin_search(arr, 7)}")
print(f"   Search 6 in {arr}: index {bin_search(arr, 6)}")


# 6. Tower of Hanoi
def hanoi(n, source, dest, aux):
    if n == 1:
        print(f"   Move disk 1: {source} → {dest}")
        return
    hanoi(n-1, source, aux, dest)
    print(f"   Move disk {n}: {source} → {dest}")
    hanoi(n-1, aux, dest, source)

print("\n6. Tower of Hanoi (3 disks)")
hanoi(3, "A", "C", "B")
print(f"   Minimum moves for n disks: 2^n - 1")


# 7. Flatten a nested list
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

nested = [1, [2, 3], [4, [5, 6]], [7, [8, [9]]]]
print(f"\n7. Flatten {nested}:")
print(f"   Result: {flatten(nested)}")


# ────────────────────────────────────────────────────────────
#  BACKTRACKING
# ────────────────────────────────────────────────────────────

print("\n\n" + "=" * 55)
print("  BACKTRACKING")
print("=" * 55)


# 1. Generate all subsets (Power Set)
def subsets(nums):
    result = []
    def backtrack(start, current):
        result.append(current[:])      # add snapshot
        for i in range(start, len(nums)):
            current.append(nums[i])    # choose
            backtrack(i + 1, current)  # explore
            current.pop()              # un-choose (backtrack)
    backtrack(0, [])
    return result

nums = [1, 2, 3]
all_subsets = subsets(nums)
print(f"\n1. Subsets of {nums}:")
print(f"   {all_subsets}")
print(f"   Total: {len(all_subsets)} (= 2^{len(nums)})")


# 2. Permutations
def permutations(nums):
    result = []
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
    backtrack([], nums)
    return result

nums2 = [1, 2, 3]
perms = permutations(nums2)
print(f"\n2. Permutations of {nums2}:")
for p in perms: print(f"   {p}")
print(f"   Total: {len(perms)} (= {len(nums2)}!)")


# 3. Combinations
def combinations(nums, k):
    result = []
    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result

nums3 = [1, 2, 3, 4]
k = 2
print(f"\n3. Combinations of {nums3} choose {k}:")
print(f"   {combinations(nums3, k)}")


# 4. N-Queens Problem
def n_queens(n):
    """Place N queens on N×N board so no two attack each other."""
    results = []

    def is_safe(board, row, col):
        # Check column
        for r in range(row):
            if board[r] == col: return False
        # Check diagonals
        for r in range(row):
            if abs(board[r] - col) == abs(r - row): return False
        return True

    def backtrack(board, row):
        if row == n:
            results.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1   # backtrack

    backtrack([-1]*n, 0)

    def draw_board(solution):
        lines = []
        for row in solution:
            line = ". " * row + "Q " + ". " * (n - row - 1)
            lines.append("   " + line.strip())
        return "\n".join(lines)

    return results, draw_board

results, draw = n_queens(4)
print(f"\n4. {4}-Queens Problem:")
print(f"   Found {len(results)} solution(s)")
print(f"\n   Solution 1:")
print(draw(results[0]))
if len(results) > 1:
    print(f"\n   Solution 2:")
    print(draw(results[1]))

print(f"\n   Solutions per board size:")
for size in range(1, 9):
    r, _ = n_queens(size)
    print(f"   {size}×{size}: {len(r)} solution(s)")


# 5. Maze Solver
def solve_maze(maze):
    """Find path from top-left to bottom-right in a 0/1 maze."""
    rows, cols = len(maze), len(maze[0])
    path = []
    visited = [[False]*cols for _ in range(rows)]

    def backtrack(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols: return False
        if maze[r][c] == 1 or visited[r][c]: return False   # wall or visited
        visited[r][c] = True
        path.append((r, c))
        if r == rows-1 and c == cols-1: return True   # reached goal
        if backtrack(r+1,c) or backtrack(r,c+1) or backtrack(r-1,c) or backtrack(r,c-1):
            return True
        path.pop()          # backtrack
        return False

    found = backtrack(0, 0)
    return path if found else None

maze = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
path = solve_maze(maze)
print(f"\n5. Maze Solver (0=open, 1=wall):")
for row in maze:
    print("  ", " ".join("█" if c else "." for c in row))
if path:
    print(f"\n   Path found ({len(path)} steps):")
    print(f"   {path}")
else:
    print("   No path found!")


# 6. Sudoku Solver
def solve_sudoku(board):
    """Solve 9×9 sudoku using backtracking."""
    def is_valid(board, row, col, num):
        if num in board[row]: return False
        if num in [board[r][col] for r in range(9)]: return False
        br, bc = (row//3)*3, (col//3)*3
        for r in range(br, br+3):
            for c in range(bc, bc+3):
                if board[r][c] == num: return False
        return True

    def backtrack():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if backtrack(): return True
                            board[row][col] = 0   # backtrack
                    return False
        return True

    import copy
    b = copy.deepcopy(board)
    solved = backtrack.__wrapped__ if hasattr(backtrack, '__wrapped__') else backtrack
    # Re-define with proper scope
    def backtrack2():
        for row in range(9):
            for col in range(9):
                if b[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(b, row, col, num):
                            b[row][col] = num
                            if backtrack2(): return True
                            b[row][col] = 0
                    return False
        return True

    backtrack2()
    return b

sudoku = [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],
    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],
    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9],
]
print(f"\n6. Sudoku Solver")
solution = solve_sudoku(sudoku)
print("   Solved:")
for row in solution:
    print("  ", " ".join(str(x) for x in row))
