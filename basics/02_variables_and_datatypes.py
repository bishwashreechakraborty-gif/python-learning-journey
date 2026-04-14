# 02_variables_and_datatypes.py — Learn about variables and data types

# ── String ──────────────────────────────
name = "Alice"
print("Name:", name)
print("Type:", type(name))

# ── Integer ─────────────────────────────
age = 25
print("\nAge:", age)
print("Type:", type(age))

# ── Float ───────────────────────────────
height = 5.6
print("\nHeight:", height)
print("Type:", type(height))

# ── Boolean ─────────────────────────────
is_student = True
print("\nIs student:", is_student)
print("Type:", type(is_student))

# ── Basic Math with variables ────────────
x = 10
y = 3
print("\n--- Basic Math ---")
print("Addition:", x + y)
print("Subtraction:", x - y)
print("Multiplication:", x * y)
print("Division:", x / y)
print("Floor Division:", x // y)
print("Modulus (remainder):", x % y)
print("Power:", x ** y)

# ── String operations ────────────────────
first = "Hello"
second = "Python"
print("\n--- String Operations ---")
print(first + " " + second)           # Concatenation
print(first * 3)                       # Repeat
print("Length of name:", len(name))   # Length
print(name.upper())                    # Uppercase
print(name.lower())                    # Lowercase
