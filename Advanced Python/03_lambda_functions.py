# ============================================================
#  Topic 3: Lambda Functions
#  Covers: syntax, map, filter, reduce, sorted, real use cases
# ============================================================

from functools import reduce

# ── 1. Lambda Syntax ─────────────────────────────────────
print("=== 1. Lambda Syntax ===")

# lambda arguments: expression
square    = lambda x: x ** 2
add       = lambda x, y: x + y
greet     = lambda name, msg="Hello": f"{msg}, {name}!"
is_even   = lambda x: x % 2 == 0

print(f"  square(7)        = {square(7)}")
print(f"  add(3, 4)        = {add(3, 4)}")
print(f"  greet('Alice')   = {greet('Alice')}")
print(f"  greet('Bob','Hi')= {greet('Bob', 'Hi')}")
print(f"  is_even(4)       = {is_even(4)}")

# ── 2. map() ─────────────────────────────────────────────
print("\n=== 2. map() ===")
# map(function, iterable) → applies function to every element

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squares    = list(map(lambda x: x**2, numbers))
doubled    = list(map(lambda x: x * 2, numbers))
to_strings = list(map(str, numbers))

print(f"  numbers  : {numbers}")
print(f"  squares  : {squares}")
print(f"  doubled  : {doubled}")
print(f"  strings  : {to_strings}")

# map with multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(f"\n  a={a}, b={b}")
print(f"  map(add) : {sums}")

# Practical: convert Celsius to Fahrenheit
celsius    = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: round(c * 9/5 + 32, 1), celsius))
print(f"\n  Celsius   : {celsius}")
print(f"  Fahrenheit: {fahrenheit}")


# ── 3. filter() ──────────────────────────────────────────
print("\n=== 3. filter() ===")
# filter(function, iterable) → keeps elements where function returns True

nums = list(range(-5, 11))
evens    = list(filter(lambda x: x % 2 == 0, nums))
positives= list(filter(lambda x: x > 0, nums))
big_even = list(filter(lambda x: x % 2 == 0 and x > 5, nums))

print(f"  nums     : {nums}")
print(f"  evens    : {evens}")
print(f"  positives: {positives}")
print(f"  big evens: {big_even}")

# Practical: filter valid emails
emails = ["alice@gmail.com", "invalid-email", "bob@yahoo.com", "", "carol@company.in"]
valid = list(filter(lambda e: "@" in e and "." in e.split("@")[-1], emails))
print(f"\n  All emails  : {emails}")
print(f"  Valid emails: {valid}")


# ── 4. reduce() ──────────────────────────────────────────
print("\n=== 4. reduce() ===")
# reduce(function, iterable) → accumulates result left to right

nums = [1, 2, 3, 4, 5]
total   = reduce(lambda acc, x: acc + x,    nums)
product = reduce(lambda acc, x: acc * x,    nums)
maximum = reduce(lambda a, b: a if a > b else b, nums)

print(f"  nums    : {nums}")
print(f"  sum     : {total}")
print(f"  product : {product}")
print(f"  maximum : {maximum}")

# With initial value
total_with_init = reduce(lambda acc, x: acc + x, nums, 100)
print(f"  sum + 100 initial: {total_with_init}")


# ── 5. sorted() with lambda key ──────────────────────────
print("\n=== 5. sorted() with Lambda Key ===")

# Sort strings by length
words = ["banana", "fig", "apple", "kiwi", "cherry", "date"]
by_len  = sorted(words, key=lambda w: len(w))
by_last = sorted(words, key=lambda w: w[-1])
rev_len = sorted(words, key=lambda w: len(w), reverse=True)

print(f"  words   : {words}")
print(f"  by len  : {by_len}")
print(f"  by last : {by_last}")
print(f"  rev len : {rev_len}")

# Sort list of dicts
students = [
    {"name": "Alice", "age": 20, "gpa": 3.8},
    {"name": "Bob",   "age": 22, "gpa": 3.5},
    {"name": "Carol", "age": 19, "gpa": 3.9},
    {"name": "David", "age": 21, "gpa": 3.5},
]
by_gpa  = sorted(students, key=lambda s: s["gpa"], reverse=True)
by_name = sorted(students, key=lambda s: s["name"])
by_age_gpa = sorted(students, key=lambda s: (s["age"], -s["gpa"]))

print(f"\n  By GPA (desc)  : {[s['name'] for s in by_gpa]}")
print(f"  By name (asc)  : {[s['name'] for s in by_name]}")
print(f"  By age, then GPA: {[(s['name'], s['age']) for s in by_age_gpa]}")


# ── 6. Lambda in higher-order functions ──────────────────
print("\n=== 6. Lambda in HOF ===")

def apply_twice(func, value):
    return func(func(value))

def compose(f, g):
    return lambda x: f(g(x))

double   = lambda x: x * 2
add_ten  = lambda x: x + 10

print(f"  apply_twice(double, 3)  = {apply_twice(double, 3)}")
print(f"  apply_twice(add_ten, 5) = {apply_twice(add_ten, 5)}")

double_then_add = compose(add_ten, double)
add_then_double = compose(double, add_ten)
print(f"  double then add 10 to 5: {double_then_add(5)}")
print(f"  add 10 then double to 5: {add_then_double(5)}")


# ── 7. Practical use cases ────────────────────────────────
print("\n=== 7. Practical Use Cases ===")

# 7a. Group by condition
transactions = [
    {"amount": 150, "type": "credit"},
    {"amount":  50, "type": "debit"},
    {"amount": 300, "type": "credit"},
    {"amount":  80, "type": "debit"},
]
credits = list(filter(lambda t: t["type"] == "credit", transactions))
debits  = list(filter(lambda t: t["type"] == "debit",  transactions))
net     = reduce(lambda a, t: a + (t["amount"] if t["type"]=="credit" else -t["amount"]), transactions, 0)
print(f"  Credits: ₹{sum(t['amount'] for t in credits)}")
print(f"  Debits : ₹{sum(t['amount'] for t in debits)}")
print(f"  Net    : ₹{net}")

# 7b. Word frequency
words2 = ["apple", "banana", "apple", "cherry", "banana", "apple"]
freq = reduce(lambda d, w: {**d, w: d.get(w, 0) + 1}, words2, {})
sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
print(f"\n  Word frequency: {sorted_freq}")

# 7c. Pipeline with map+filter+reduce
data = list(range(1, 21))
result = reduce(
    lambda acc, x: acc + x,
    filter(lambda x: x % 2 == 0,       # keep evens
    map(lambda x: x ** 2, data)),       # square all
    0
)
print(f"\n  Sum of squares of even numbers 1–20: {result}")


# ── 8. Lambda vs def ─────────────────────────────────────
print("\n=== 8. Lambda vs def — When to Use Which ===")
print("""
  USE LAMBDA when:
  ✅ Short, one-line, throwaway functions
  ✅ Passing as argument to map/filter/sorted/reduce
  ✅ Simple key functions

  USE def when:
  ✅ Function needs a name (reused multiple times)
  ✅ Needs docstring
  ✅ Multi-line logic
  ✅ Needs default args, *args, **kwargs
  ✅ Needs return type hints
""")
