# ============================================================
#  PHASE 2 — Topic 2: Modules & Packages
#  Covers: built-in modules, importing, creating your own
# ============================================================

# ── 1. math module ────────────────────────────────────────
import math

print("=== math module ===")
print("Pi:", math.pi)
print("e:", math.e)
print("Square root of 25:", math.sqrt(25))
print("Ceiling of 4.3:", math.ceil(4.3))
print("Floor of 4.7:", math.floor(4.7))
print("2^10:", math.pow(2, 10))
print("log10(1000):", math.log10(1000))
print("sin(90°):", math.sin(math.radians(90)))


# ── 2. random module ─────────────────────────────────────
import random

print("\n=== random module ===")
print("Random int (1-10):", random.randint(1, 10))
print("Random float (0-1):", round(random.random(), 4))
print("Random choice:", random.choice(["apple", "banana", "cherry"]))

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
random.shuffle(cards)
print("Shuffled cards (first 5):", cards[:5])

sample = random.sample(range(1, 50), 6)   # like a lottery
print("Lucky numbers:", sorted(sample))


# ── 3. datetime module ────────────────────────────────────
from datetime import datetime, date, timedelta

print("\n=== datetime module ===")
now = datetime.now()
print("Now:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("Date only:", date.today())
print("Year:", now.year, "| Month:", now.month, "| Day:", now.day)

future = date.today() + timedelta(days=30)
print("30 days from now:", future)

birthday = date(2000, 8, 15)
today = date.today()
age_days = (today - birthday).days
print(f"Days since Aug 15 2000: {age_days} days (~{age_days // 365} years)")


# ── 4. os module ─────────────────────────────────────────
import os

print("\n=== os module ===")
print("Current directory:", os.getcwd())
print("Directory contents:", os.listdir(".")[:5])  # first 5 items
print("OS name:", os.name)
print("Path separator:", os.sep)

# Build paths safely (works on Windows and Mac/Linux)
folder = "my_folder"
filename = "data.txt"
full_path = os.path.join(folder, filename)
print("Joined path:", full_path)
print("Does this file exist?", os.path.exists(full_path))


# ── 5. sys module ────────────────────────────────────────
import sys

print("\n=== sys module ===")
print("Python version:", sys.version[:6])
print("Platform:", sys.platform)
print("Max integer:", sys.maxsize)


# ── 6. string module ─────────────────────────────────────
import string

print("\n=== string module ===")
print("Lowercase:", string.ascii_lowercase)
print("Uppercase:", string.ascii_uppercase)
print("Digits:", string.digits)
print("Punctuation:", string.punctuation)


# ── 7. json module ────────────────────────────────────────
import json

print("\n=== json module ===")
data = {"name": "Alice", "age": 25, "skills": ["Python", "SQL"]}

# Python dict → JSON string
json_str = json.dumps(data, indent=2)
print("Dict to JSON:\n", json_str)

# JSON string → Python dict
parsed = json.loads(json_str)
print("Back to dict:", parsed)
print("Name from parsed:", parsed["name"])

# Save to file
with open("sample_data.json", "w") as f:
    json.dump(data, f, indent=2)
print("Saved to sample_data.json ✅")

# Load from file
with open("sample_data.json", "r") as f:
    loaded = json.load(f)
print("Loaded from file:", loaded)


# ── 8. Selective imports ──────────────────────────────────
from math import sqrt, pi
from random import randint, choice

print("\n=== Selective imports ===")
print("sqrt(144):", sqrt(144))
print("pi:", pi)
print("Random 1-6 (dice):", randint(1, 6))
print("Random color:", choice(["red", "green", "blue"]))


# ── 9. Aliased imports ────────────────────────────────────
import datetime as dt
import os.path as osp

print("\n=== Aliased imports ===")
print("Today:", dt.date.today())
print("Path exists:", osp.exists("."))


# ── 10. Creating a custom module ─────────────────────────
# Save this as myutils.py in the same folder and import it:
#
#   from myutils import greet, square
#
# Contents of myutils.py would be:
#   def greet(name): return f"Hello, {name}!"
#   def square(n):   return n ** 2
#
# Then use it like:
#   print(greet("Alice"))   → Hello, Alice!
#   print(square(5))        → 25

print("\n=== Custom Module Example ===")
print("Create a file called 'myutils.py' with your own functions,")
print("then import and use them just like any built-in module!")
