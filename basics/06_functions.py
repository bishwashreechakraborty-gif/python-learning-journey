# 06_functions.py — Learn how to create and use functions

# ── Basic function ────────────────────────
def greet():
    print("Hello! Welcome to Python functions.")

greet()   # Call the function

# ── Function with parameter ───────────────
def greet_person(name):
    print(f"Hello, {name}! Nice to meet you.")

greet_person("Alice")
greet_person("Bob")

# ── Function that returns a value ─────────
def add(a, b):
    return a + b

result = add(5, 3)
print("\n5 + 3 =", result)

# ── Function with default value ───────────
def power(base, exponent=2):
    return base ** exponent

print("3^2 =", power(3))        # uses default exponent
print("2^5 =", power(2, 5))     # custom exponent

# ── Practical functions ───────────────────
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

temp_c = float(input("\nEnter temperature in Celsius: "))
print(f"{temp_c}°C = {celsius_to_fahrenheit(temp_c):.1f}°F")

temp_f = float(input("Enter temperature in Fahrenheit: "))
print(f"{temp_f}°F = {fahrenheit_to_celsius(temp_f):.1f}°C")

# ── Function with multiple returns ────────
def min_max(numbers):
    return min(numbers), max(numbers)

nums = [4, 7, 1, 9, 2, 5]
smallest, largest = min_max(nums)
print(f"\nList: {nums}")
print(f"Smallest: {smallest}, Largest: {largest}")

# ── Recursive function ────────────────────
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

num = int(input("\nEnter a number to find its factorial: "))
print(f"{num}! = {factorial(num)}")
