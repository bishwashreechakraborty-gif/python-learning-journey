# ============================================================
#  Topic 2: Generators
#  Covers: yield, generator functions, expressions,
#          send(), pipeline, infinite sequences, memory savings
# ============================================================

import sys

# ── 1. Generator vs Regular Function ──────────────────────
print("=== 1. Generator vs List ===")

def regular_squares(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result   # builds entire list in memory

def gen_squares(n):
    for i in range(n):
        yield i ** 2   # produces one value at a time

# Memory comparison
n = 10_000
list_size = sys.getsizeof(regular_squares(n))
gen_size  = sys.getsizeof(gen_squares(n))
print(f"  List size:      {list_size:,} bytes")
print(f"  Generator size: {gen_size:,} bytes")
print(f"  Memory saved:   {list_size - gen_size:,} bytes")

print(f"\n  First 5 squares: {[next(gen_squares(10)) for _ in range(1)]}")
print(f"  All squares 0–9: {list(gen_squares(10))}")


# ── 2. Generator with multiple yields ─────────────────────
print("\n=== 2. Multiple Yields ===")

def count_up_down(n):
    print("  Counting up...")
    for i in range(n):
        yield i
    print("  Counting down...")
    for i in range(n, -1, -1):
        yield i

gen = count_up_down(3)
for val in gen:
    print(f"  {val}", end=" ")
print()


# ── 3. Generator with state ───────────────────────────────
print("\n=== 3. Stateful Generator (Fibonacci) ===")

def fibonacci():
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
first_15 = [next(fib) for _ in range(15)]
print(f"  First 15 Fibonacci: {first_15}")


# ── 4. Generator expressions ─────────────────────────────
print("\n=== 4. Generator Expressions ===")

# List comprehension — builds full list
squares_list = [x**2 for x in range(10)]

# Generator expression — lazy, no list built
squares_gen = (x**2 for x in range(10))

print(f"  List comprehension: {squares_list}")
print(f"  Generator expr type: {type(squares_gen)}")
print(f"  Consumed: {list(squares_gen)}")

# Chained generator expressions (pipeline)
numbers   = range(1, 21)
evens     = (x for x in numbers if x % 2 == 0)
squared   = (x**2 for x in evens)
over_100  = (x for x in squared if x > 100)
print(f"\n  Pipeline (even²>100 from 1–20): {list(over_100)}")

# Sum without creating a list
total = sum(x**2 for x in range(1_000_000))
print(f"  Sum of squares 0–999999: {total:,} (computed lazily)")


# ── 5. yield from (delegation) ───────────────────────────
print("\n=== 5. yield from ===")

def chain(*iterables):
    for it in iterables:
        yield from it        # delegates to sub-generator

result = list(chain([1,2,3], "abc", range(4, 7)))
print(f"  Chain: {result}")

def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, 3], [4, [5, 6]], [7, [8, [9]]]]
print(f"  Flatten: {list(flatten(nested))}")


# ── 6. send() — two-way communication ────────────────────
print("\n=== 6. send() — Two-way Communication ===")

def accumulator():
    total = 0
    while True:
        value = yield total   # yields total, receives next value
        if value is None: break
        total += value

acc = accumulator()
next(acc)           # prime the generator
print(f"  Send 10: {acc.send(10)}")
print(f"  Send 25: {acc.send(25)}")
print(f"  Send  5: {acc.send(5)}")


# ── 7. Practical: File reader generator ──────────────────
print("\n=== 7. Practical: Large File Reader ===")

# Simulate writing a large CSV
with open("temp_data.csv", "w") as f:
    f.write("name,score\n")
    for i in range(1000):
        f.write(f"student_{i},{i % 100}\n")

def read_csv_rows(filename, skip_header=True):
    """Memory-efficient CSV reader — one row at a time."""
    with open(filename) as f:
        if skip_header: next(f)
        for line in f:
            yield line.strip().split(",")

def filter_rows(rows, col_idx, min_val):
    for row in rows:
        if float(row[col_idx]) >= min_val:
            yield row

# Pipeline: read → filter → process
rows    = read_csv_rows("temp_data.csv")
passing = filter_rows(rows, 1, 90)
top     = [row for _, row in zip(range(5), passing)]

print(f"  Top 5 students with score ≥ 90:")
for row in top:
    print(f"    {row[0]}: {row[1]}")

import os; os.remove("temp_data.csv")


# ── 8. Infinite generators ────────────────────────────────
print("\n=== 8. Infinite Generators ===")

def naturals(start=1):
    n = start
    while True:
        yield n
        n += 1

def take(n, gen):
    return [next(gen) for _ in range(n)]

def primes():
    """Infinite prime number generator using sieve."""
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True
    n = 2
    while True:
        if is_prime(n): yield n
        n += 1

print(f"  First 10 naturals: {take(10, naturals())}")
print(f"  First 15 primes:   {take(15, primes())}")


# ── 9. Generator as context manager ──────────────────────
print("\n=== 9. Generator as Context Manager ===")

from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"  📂 Opening {name}")
    resource = {"name": name, "data": []}
    try:
        yield resource
    except Exception as e:
        print(f"  ❌ Error: {e}")
    finally:
        print(f"  🔒 Closing {name}")

with managed_resource("database connection") as res:
    res["data"].append("record 1")
    res["data"].append("record 2")
    print(f"  Data: {res['data']}")


# ── 10. Performance summary ───────────────────────────────
print("\n=== 10. Generator Performance Summary ===")
print("""
  When to use generators:
  ✅ Large datasets that don't fit in memory
  ✅ Streaming data (files, network, APIs)
  ✅ Infinite sequences (IDs, timestamps, sensors)
  ✅ Pipeline/chaining operations
  ✅ Lazy evaluation (compute only when needed)

  Key keywords:
  • yield          → produce a value, pause function
  • yield from     → delegate to another iterable
  • next(gen)      → get next value
  • gen.send(val)  → send value into generator
  • StopIteration  → raised when generator is exhausted
""")
