# 04_loops.py — Learn for loops and while loops

# ── for loop: count from 1 to 5 ──────────
print("── for loop: 1 to 5 ──")
for i in range(1, 6):
    print(i)

# ── for loop: loop through a list ────────
print("\n── Loop through fruits ──")
fruits = ["apple", "banana", "cherry", "mango"]
for fruit in fruits:
    print("Fruit:", fruit)

# ── for loop: multiplication table ───────
num = int(input("\nEnter a number for its multiplication table: "))
print(f"\n── Multiplication Table of {num} ──")
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

# ── while loop: countdown ─────────────────
print("\n── Countdown ──")
count = 5
while count > 0:
    print(count)
    count -= 1
print("Blast off! 🚀")

# ── while loop: sum of numbers ────────────
print("\n── Sum numbers until you type 0 ──")
total = 0
while True:
    n = int(input("Enter a number (0 to stop): "))
    if n == 0:
        break
    total += n
print(f"Total sum: {total}")

# ── Nested loop: pattern ─────────────────
print("\n── Star Pattern ──")
for row in range(1, 6):
    print("* " * row)

# ── continue: skip even numbers ──────────
print("\n── Odd numbers from 1 to 10 ──")
for i in range(1, 11):
    if i % 2 == 0:
        continue       # skip even
    print(i)
