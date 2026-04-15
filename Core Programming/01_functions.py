# ============================================================
#  Topic 1: Functions
#  Covers: arguments, return values, *args/**kwargs, recursion
# ============================================================

# ── 1. Basic function ─────────────────────────────────────
def greet():
    print("Hello! I am a basic function.")

greet()


# ── 2. Function with positional arguments ────────────────
def add(a, b):
    return a + b

print("\n5 + 3 =", add(5, 3))


# ── 3. Function with default arguments ───────────────────
def greet_user(name, message="Welcome to Python!"):
    print(f"Hello {name}! {message}")

greet_user("Alice")
greet_user("Bob", "Great to see you!")


# ── 4. Function with keyword arguments ───────────────────
def student_info(name, age, grade):
    print(f"Name: {name} | Age: {age} | Grade: {grade}")

student_info(age=20, grade="A", name="Carol")   # order doesn't matter


# ── 5. *args — variable number of positional arguments ───
def total(*numbers):
    print(f"Numbers received: {numbers}")
    return sum(numbers)

print("\nSum of 1,2,3:", total(1, 2, 3))
print("Sum of 1..5:", total(1, 2, 3, 4, 5))


# ── 6. **kwargs — variable number of keyword arguments ───
def display_profile(**details):
    print("\nProfile:")
    for key, value in details.items():
        print(f"  {key}: {value}")

display_profile(name="Alice", city="Delhi", hobby="Coding")


# ── 7. Function returning multiple values ─────────────────
def min_max_avg(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

nums = [4, 7, 2, 9, 1, 5]
lo, hi, avg = min_max_avg(nums)
print(f"\nList: {nums}")
print(f"Min: {lo} | Max: {hi} | Avg: {avg:.2f}")


# ── 8. Lambda (anonymous) functions ──────────────────────
square   = lambda x: x ** 2
multiply = lambda x, y: x * y

print("\nSquare of 6:", square(6))
print("3 × 4:", multiply(3, 4))

numbers = [5, 2, 8, 1, 9]
numbers.sort(key=lambda x: x)
print("Sorted:", numbers)


# ── 9. Recursion ──────────────────────────────────────────
# Factorial: n! = n × (n-1) × ... × 1
def factorial(n):
    if n == 0 or n == 1:          # Base case
        return 1
    return n * factorial(n - 1)  # Recursive call

print("\n--- Factorial using Recursion ---")
for i in range(1, 8):
    print(f"  {i}! = {factorial(i)}")


# Fibonacci: 0, 1, 1, 2, 3, 5, 8, ...
def fibonacci(n):
    if n <= 0: return 0
    if n == 1: return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print("\n--- Fibonacci Sequence (first 10) ---")
print([fibonacci(i) for i in range(10)])


# ── 10. Scope: Local vs Global ────────────────────────────
count = 0   # Global variable

def increment():
    global count
    count += 1

increment()
increment()
increment()
print(f"\nGlobal count after 3 increments: {count}")


# ── 11. Nested functions ──────────────────────────────────
def outer(x):
    def inner(y):
        return x + y    # inner can access outer's variables
    return inner

add_five = outer(5)
print("\nNested function — add_five(3):", add_five(3))
