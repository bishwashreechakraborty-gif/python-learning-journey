# 03_input_and_conditions.py — Taking user input and using if/else

# ── Get input from user ──────────────────
name = input("What is your name? ")
age = int(input("How old are you? "))

print(f"\nHello, {name}!")

# ── if / elif / else ─────────────────────
if age < 13:
    print("You are a child.")
elif age < 18:
    print("You are a teenager.")
elif age < 60:
    print("You are an adult.")
else:
    print("You are a senior citizen.")

# ── Check if number is even or odd ───────
number = int(input("\nEnter a number: "))

if number % 2 == 0:
    print(f"{number} is Even.")
else:
    print(f"{number} is Odd.")

# ── Simple grade checker ─────────────────
score = int(input("\nEnter your exam score (0-100): "))

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")

# ── and / or operators ───────────────────
has_id = input("\nDo you have an ID? (yes/no): ").lower()
has_ticket = input("Do you have a ticket? (yes/no): ").lower()

if has_id == "yes" and has_ticket == "yes":
    print("Welcome! You may enter.")
else:
    print("Sorry, you cannot enter.")
