# ============================================================
#  Topic 2: Constructors (__init__)
#  Covers: __init__, default params, chained constructors,
#          __del__, __new__, multiple ways to initialise
# ============================================================

# ── 1. Basic __init__ ─────────────────────────────────────
print("=== 1. Basic __init__ ===")

class Person:
    def __init__(self, name, age):
        print(f"  🔨 Creating Person: {name}")
        self.name = name
        self.age  = age

    def greet(self):
        return f"Hi, I'm {self.name}, {self.age} years old."

p1 = Person("Alice", 25)
p2 = Person("Bob",   30)
print(p1.greet())
print(p2.greet())


# ── 2. Default parameter values ───────────────────────────
print("\n=== 2. Default Parameters ===")

class Car:
    def __init__(self, brand, model, year=2024, color="White", fuel="Petrol"):
        self.brand = brand
        self.model = model
        self.year  = year
        self.color = color
        self.fuel  = fuel

    def __str__(self):
        return f"{self.year} {self.color} {self.brand} {self.model} ({self.fuel})"

c1 = Car("Toyota", "Innova")                         # uses all defaults
c2 = Car("Honda",  "City", 2022, "Red")              # overrides some
c3 = Car("Tesla",  "Model 3", 2023, "Black", "EV")  # overrides all
print(c1)
print(c2)
print(c3)


# ── 3. __init__ with validation ───────────────────────────
print("\n=== 3. Validation in __init__ ===")

class BankAccount:
    def __init__(self, owner, balance=0.0):
        if not owner or not isinstance(owner, str):
            raise ValueError("Owner name must be a non-empty string.")
        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.owner   = owner
        self.balance = float(balance)
        print(f"  ✅ Account created for '{owner}' with ₹{self.balance:.2f}")

try:
    a1 = BankAccount("Alice", 1000)
    a2 = BankAccount("Bob")               # default balance 0
    a3 = BankAccount("Carol", -500)       # raises ValueError
except ValueError as e:
    print(f"  ❌ Error: {e}")


# ── 4. __init__ with mutable default (correct pattern) ────
print("\n=== 4. Mutable Defaults (use None, not []) ===")

class Student:
    def __init__(self, name, subjects=None):
        self.name     = name
        # CORRECT: never use [] as default — it's shared across objects!
        self.subjects = subjects if subjects is not None else []

    def add_subject(self, subject):
        self.subjects.append(subject)

    def __str__(self):
        return f"{self.name}: {self.subjects}"

s1 = Student("Alice")
s2 = Student("Bob")
s1.add_subject("Math")
s1.add_subject("Python")
s2.add_subject("History")

print(s1)     # Alice: ['Math', 'Python']
print(s2)     # Bob:   ['History']  ← NOT shared with Alice ✅


# ── 5. @classmethod as alternative constructors ───────────
print("\n=== 5. Alternative Constructors with @classmethod ===")

class Date:
    def __init__(self, day, month, year):
        self.day   = day
        self.month = month
        self.year  = year

    @classmethod
    def from_string(cls, date_str):
        """Create Date from 'DD-MM-YYYY' string."""
        day, month, year = map(int, date_str.split("-"))
        return cls(day, month, year)

    @classmethod
    def today(cls):
        """Create Date from today's date."""
        from datetime import date
        d = date.today()
        return cls(d.day, d.month, d.year)

    def __str__(self):
        months = ["", "Jan","Feb","Mar","Apr","May","Jun",
                      "Jul","Aug","Sep","Oct","Nov","Dec"]
        return f"{self.day:02d} {months[self.month]} {self.year}"

d1 = Date(15, 8, 1947)
d2 = Date.from_string("26-01-1950")
d3 = Date.today()

print("d1 =", d1)
print("d2 =", d2)
print("d3 =", d3)


# ── 6. __del__ (destructor) ───────────────────────────────
print("\n=== 6. __del__ (destructor) ===")

class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        print(f"  📂 Opening '{filename}'")

    def read(self):
        return f"  📖 Reading '{self.filename}'..."

    def __del__(self):
        print(f"  🔒 Closing '{self.filename}' (destructor called)")

fh = FileHandler("data.txt")
print(fh.read())
del fh     # manually triggers __del__
print("  (FileHandler deleted)")


# ── 7. Copying objects ────────────────────────────────────
print("\n=== 7. Shallow vs Deep Copy ===")
import copy

class Config:
    def __init__(self, settings):
        self.settings = settings    # mutable dict

cfg1 = Config({"debug": True, "theme": "dark"})
cfg2 = cfg1                         # same reference — NOT a copy!
cfg3 = copy.copy(cfg1)              # shallow copy
cfg4 = copy.deepcopy(cfg1)         # deep copy (fully independent)

cfg2.settings["theme"] = "light"   # also changes cfg1!
cfg3.settings["debug"] = False     # also changes cfg1 (shallow)!
cfg4.settings["theme"] = "blue"    # independent ✅

print(f"cfg1 settings: {cfg1.settings}")   # changed by cfg2 and cfg3
print(f"cfg4 settings: {cfg4.settings}")   # fully independent
print("  → Use copy.deepcopy() for fully independent copies!")
