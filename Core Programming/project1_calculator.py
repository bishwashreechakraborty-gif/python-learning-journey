# ============================================================
#  PHASE 2 — Project 1: Calculator
#  Features: basic ops, power, sqrt, log, history, exception
#            handling, modular functions, loop menu
# ============================================================

import math
import os

# ── Store calculation history ─────────────────────────────
history = []

# ────────────────────────────────────────────────────────────
#  CORE FUNCTIONS
# ────────────────────────────────────────────────────────────

def add(a, b):        return a + b
def subtract(a, b):   return a - b
def multiply(a, b):   return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

def power(a, b):      return a ** b

def square_root(a):
    if a < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(a)

def logarithm(a, base=10):
    if a <= 0:
        raise ValueError("Logarithm input must be positive.")
    if base <= 0 or base == 1:
        raise ValueError("Logarithm base must be > 0 and not 1.")
    return math.log(a, base)

def modulus(a, b):
    if b == 0:
        raise ZeroDivisionError("Modulus by zero is not allowed.")
    return a % b


# ────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ────────────────────────────────────────────────────────────

def get_number(prompt):
    """Prompt until a valid number is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ❌ Invalid number. Please try again.")

def log_history(expression, result):
    """Save calculation to history."""
    entry = f"{expression} = {result}"
    history.append(entry)

def show_history():
    """Display all past calculations."""
    if not history:
        print("\n  📭 No history yet.")
        return
    print("\n  📋 Calculation History:")
    for i, entry in enumerate(history, 1):
        print(f"    {i}. {entry}")

def save_history():
    """Save history to a text file."""
    if not history:
        print("  ❌ Nothing to save.")
        return
    with open("calculator_history.txt", "a") as f:
        f.write("\n".join(history) + "\n")
    print("  ✅ History saved to 'calculator_history.txt'")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_menu():
    print("\n" + "=" * 42)
    print("        🧮  PYTHON CALCULATOR")
    print("=" * 42)
    print("  Basic Operations:")
    print("   [1]  Addition         (+)")
    print("   [2]  Subtraction      (−)")
    print("   [3]  Multiplication   (×)")
    print("   [4]  Division         (÷)")
    print("   [5]  Modulus          (%)")
    print("  Advanced:")
    print("   [6]  Power            (x^y)")
    print("   [7]  Square Root      (√x)")
    print("   [8]  Logarithm        (log)")
    print("  Options:")
    print("   [9]  View History")
    print("  [10]  Save History to File")
    print("  [11]  Clear Screen")
    print("   [0]  Exit")
    print("=" * 42)


# ────────────────────────────────────────────────────────────
#  MAIN LOOP
# ────────────────────────────────────────────────────────────

def run_calculator():
    print("\n  Welcome to the Python Calculator! 🧮")
    print("  Type a menu number and press Enter.\n")

    while True:
        display_menu()
        choice = input("  Enter choice: ").strip()

        try:
            if choice == "1":
                a = get_number("  Enter first number: ")
                b = get_number("  Enter second number: ")
                result = add(a, b)
                expr = f"{a} + {b}"

            elif choice == "2":
                a = get_number("  Enter first number: ")
                b = get_number("  Enter second number: ")
                result = subtract(a, b)
                expr = f"{a} - {b}"

            elif choice == "3":
                a = get_number("  Enter first number: ")
                b = get_number("  Enter second number: ")
                result = multiply(a, b)
                expr = f"{a} × {b}"

            elif choice == "4":
                a = get_number("  Enter first number: ")
                b = get_number("  Enter second number: ")
                result = divide(a, b)
                expr = f"{a} ÷ {b}"

            elif choice == "5":
                a = get_number("  Enter dividend: ")
                b = get_number("  Enter divisor: ")
                result = modulus(a, b)
                expr = f"{a} % {b}"

            elif choice == "6":
                a = get_number("  Enter base: ")
                b = get_number("  Enter exponent: ")
                result = power(a, b)
                expr = f"{a} ^ {b}"

            elif choice == "7":
                a = get_number("  Enter number: ")
                result = square_root(a)
                expr = f"√{a}"

            elif choice == "8":
                a = get_number("  Enter number: ")
                base_input = input("  Enter base (default 10): ").strip()
                base = float(base_input) if base_input else 10
                result = logarithm(a, base)
                expr = f"log{int(base)}({a})" if base == int(base) else f"log{base}({a})"

            elif choice == "9":
                show_history()
                continue

            elif choice == "10":
                save_history()
                continue

            elif choice == "11":
                clear_screen()
                continue

            elif choice == "0":
                print("\n  👋 Goodbye! Thanks for using the calculator.")
                break

            else:
                print("  ⚠️  Invalid choice. Please enter a number from the menu.")
                continue

            # Format result nicely
            if isinstance(result, float) and result == int(result):
                formatted = int(result)
            else:
                formatted = round(result, 6)

            print(f"\n  ✅  {expr} = {formatted}")
            log_history(expr, formatted)

        except (ZeroDivisionError, ValueError) as e:
            print(f"\n  ❌  Error: {e}")
        except Exception as e:
            print(f"\n  ❌  Unexpected error: {e}")


# ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_calculator()
