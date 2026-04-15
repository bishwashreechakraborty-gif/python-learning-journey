# ============================================================
#  Topic 4: Exception Handling
#  Covers: try/except, multiple exceptions, else, finally,
#          raising exceptions, custom exceptions
# ============================================================

# ── 1. Basic try / except ─────────────────────────────────
print("=== 1. Basic try / except ===")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("❌ Error: Cannot divide by zero!")

print("Program continues after handling the error ✅")


# ── 2. Catching user input errors ────────────────────────
print("\n=== 2. Handling ValueError ===")
try:
    num = int(input("Enter a number: "))
    print(f"You entered: {num}")
except ValueError:
    print("❌ That's not a valid number!")


# ── 3. Multiple except blocks ────────────────────────────
print("\n=== 3. Multiple Exceptions ===")
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("  ❌ Cannot divide by zero!")
    except TypeError:
        print("  ❌ Both values must be numbers!")
    return None

print(safe_divide(10, 2))      # works fine
print(safe_divide(10, 0))      # ZeroDivisionError
print(safe_divide(10, "a"))    # TypeError


# ── 4. except with multiple exception types ───────────────
print("\n=== 4. Catching Multiple Exceptions Together ===")
def parse_index(data, index):
    try:
        return int(data[index])
    except (IndexError, ValueError) as e:
        print(f"  ❌ Error: {e}")
        return None

items = ["10", "20", "abc", "30"]
print(parse_index(items, 1))   # valid
print(parse_index(items, 10))  # IndexError
print(parse_index(items, 2))   # ValueError


# ── 5. else block ─────────────────────────────────────────
print("\n=== 5. else Block (runs only if NO exception) ===")
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  ❌ Cannot divide by zero!")
    else:
        print(f"  ✅ Result: {a} / {b} = {result:.2f}")

divide(10, 4)
divide(10, 0)


# ── 6. finally block ──────────────────────────────────────
print("\n=== 6. finally Block (ALWAYS runs) ===")
def read_file(filename):
    f = None
    try:
        f = open(filename, "r")
        data = f.read()
        print(f"  ✅ Read {len(data)} characters from '{filename}'")
    except FileNotFoundError:
        print(f"  ❌ File '{filename}' not found!")
    finally:
        if f:
            f.close()
            print("  🔒 File closed (finally block ran)")

# Create a temp file to test
with open("temp_test.txt", "w") as f:
    f.write("Hello from exception handling demo!")

read_file("temp_test.txt")
read_file("no_such_file.txt")

import os
os.remove("temp_test.txt")


# ── 7. raise — manually raising exceptions ───────────────
print("\n=== 7. Raising Exceptions with 'raise' ===")
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer.")
    if age < 0 or age > 130:
        raise ValueError(f"Age {age} is not realistic (0–130).")
    print(f"  ✅ Age set to {age}")

for test_age in [25, -5, 200, "twenty"]:
    try:
        set_age(test_age)
    except (ValueError, TypeError) as e:
        print(f"  ❌ {e}")


# ── 8. Custom Exceptions ──────────────────────────────────
print("\n=== 8. Custom Exception Classes ===")

class InsufficientFundsError(Exception):
    """Raised when account balance is too low."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw ₹{amount}. Balance: ₹{balance}")

class NegativeAmountError(Exception):
    """Raised when a negative amount is given."""
    pass

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise NegativeAmountError("Deposit amount must be positive.")
        self.balance += amount
        print(f"  ✅ Deposited ₹{amount}. New balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            raise NegativeAmountError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        print(f"  ✅ Withdrew ₹{amount}. New balance: ₹{self.balance}")

acc = BankAccount("Alice", 1000)
operations = [
    ("deposit", 500),
    ("withdraw", 200),
    ("withdraw", 2000),
    ("deposit", -100),
    ("withdraw", 600),
]
for op, amount in operations:
    try:
        if op == "deposit":
            acc.deposit(amount)
        else:
            acc.withdraw(amount)
    except InsufficientFundsError as e:
        print(f"  ❌ {e}")
    except NegativeAmountError as e:
        print(f"  ❌ {e}")


# ── 9. Exception hierarchy ───────────────────────────────
print("\n=== 9. Exception Hierarchy (catching base class) ===")
def risky_operation(x):
    try:
        items = [1, 2, 3]
        return items[x] / (x - 2)
    except ArithmeticError as e:
        print(f"  Math error: {e}")
    except LookupError as e:
        print(f"  Lookup error: {e}")
    except Exception as e:
        print(f"  Unexpected error ({type(e).__name__}): {e}")

for val in [1, 2, 10, "a"]:
    risky_operation(val)


# ── 10. Practical: Robust input function ─────────────────
print("\n=== 10. Robust Input with Retry ===")
def get_integer(prompt, min_val=None, max_val=None, retries=3):
    for attempt in range(1, retries + 1):
        try:
            val = int(input(f"{prompt}: "))
            if min_val is not None and val < min_val:
                raise ValueError(f"Must be at least {min_val}")
            if max_val is not None and val > max_val:
                raise ValueError(f"Must be at most {max_val}")
            return val
        except ValueError as e:
            remaining = retries - attempt
            print(f"  ❌ Invalid input: {e}. {remaining} attempt(s) left.")
    print("  ⚠️  Too many failed attempts.")
    return None

score = get_integer("Enter your score", min_val=0, max_val=100)
if score is not None:
    print(f"  Your score: {score}")
