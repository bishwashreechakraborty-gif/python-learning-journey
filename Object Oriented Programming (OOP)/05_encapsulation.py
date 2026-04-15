# ============================================================
#  Topic 5: Encapsulation
#  Covers: public/protected/private, getters/setters,
#          @property, data hiding, name mangling
# ============================================================

# ── 1. Access Modifiers ───────────────────────────────────
print("=== 1. Access Modifiers ===")

class Employee:
    def __init__(self, name, department, salary):
        self.name          = name         # public   — accessible anywhere
        self._department   = department   # protected— convention: internal use
        self.__salary      = salary       # private  — name-mangled by Python

    def get_info(self):
        return (f"Name: {self.name} | "
                f"Dept: {self._department} | "
                f"Salary: ₹{self.__salary}")

    def give_raise(self, amount):
        if amount > 0:
            self.__salary += amount
            print(f"  ✅ Raise of ₹{amount} given. New salary: ₹{self.__salary}")
        else:
            print("  ❌ Raise amount must be positive.")

emp = Employee("Alice", "Engineering", 50000)
print(emp.name)             # ✅ public — works
print(emp._department)      # ⚠️  protected — works but not recommended

try:
    print(emp.__salary)     # ❌ AttributeError — private!
except AttributeError as e:
    print(f"  ❌ Direct access blocked: {e}")

# Name mangling — Python renames it to _ClassName__attr
print("  Via mangling:", emp._Employee__salary)   # works but bad practice

emp.give_raise(5000)
print(emp.get_info())


# ── 2. Getters and Setters ────────────────────────────────
print("\n=== 2. Getters & Setters ===")

class Temperature:
    def __init__(self, celsius):
        self.__celsius = None          # private
        self.set_celsius(celsius)      # validate via setter

    def get_celsius(self):
        return self.__celsius

    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C below absolute zero!")
        self.__celsius = value

    def get_fahrenheit(self):
        return self.__celsius * 9/5 + 32

    def set_fahrenheit(self, value):
        self.set_celsius((value - 32) * 5/9)

    def __str__(self):
        return f"{self.__celsius}°C  /  {self.get_fahrenheit():.1f}°F"

t = Temperature(25)
print(t)
t.set_celsius(100)
print(t)
t.set_fahrenheit(32)
print(t)
try:
    t.set_celsius(-300)
except ValueError as e:
    print(f"  ❌ {e}")


# ── 3. @property decorator ────────────────────────────────
print("\n=== 3. @property Decorator (Pythonic way) ===")

class Circle:
    def __init__(self, radius):
        self._radius = None
        self.radius = radius          # goes through setter

    @property
    def radius(self):
        """Getter — access like an attribute: c.radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter — with validation"""
        if value < 0:
            raise ValueError("Radius cannot be negative.")
        self._radius = value

    @radius.deleter
    def radius(self):
        print("  🗑️  Deleting radius")
        del self._radius

    @property
    def diameter(self):
        return self._radius * 2

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

    @property
    def circumference(self):
        import math
        return 2 * math.pi * self._radius

    def __str__(self):
        return (f"Circle(r={self.radius}) → "
                f"area={self.area:.2f}, circ={self.circumference:.2f}")

c = Circle(5)
print(c)
c.radius = 10                  # uses setter
print(f"Radius: {c.radius}")   # uses getter (looks like attribute!)
print(f"Diameter: {c.diameter}")
try:
    c.radius = -3              # triggers validation
except ValueError as e:
    print(f"  ❌ {e}")
del c.radius                   # triggers deleter


# ── 4. Full encapsulation example ─────────────────────────
print("\n=== 4. Fully Encapsulated BankAccount ===")

class BankAccount:
    __interest_rate = 0.04   # private class variable

    def __init__(self, owner, pin, balance=0):
        self.__owner   = owner
        self.__pin     = str(pin)
        self.__balance = balance
        self.__transactions = []
        self.__locked  = False

    def __verify_pin(self, pin):
        return str(pin) == self.__pin

    def __log(self, message):
        from datetime import datetime
        self.__transactions.append(
            f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        )

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance

    @classmethod
    def get_interest_rate(cls):
        return cls.__interest_rate

    def deposit(self, amount, pin):
        if self.__locked:
            print("  🔒 Account is locked.")
            return
        if not self.__verify_pin(pin):
            print("  ❌ Wrong PIN!")
            return
        if amount <= 0:
            print("  ❌ Invalid amount.")
            return
        self.__balance += amount
        self.__log(f"Deposited ₹{amount}")
        print(f"  ✅ Deposited ₹{amount}. Balance: ₹{self.__balance}")

    def withdraw(self, amount, pin):
        if self.__locked:
            print("  🔒 Account is locked.")
            return
        if not self.__verify_pin(pin):
            print("  ❌ Wrong PIN!")
            return
        if amount > self.__balance:
            print(f"  ❌ Insufficient funds. Balance: ₹{self.__balance}")
            return
        self.__balance -= amount
        self.__log(f"Withdrew ₹{amount}")
        print(f"  ✅ Withdrew ₹{amount}. Balance: ₹{self.__balance}")

    def change_pin(self, old_pin, new_pin):
        if not self.__verify_pin(old_pin):
            print("  ❌ Wrong current PIN!")
            return
        self.__pin = str(new_pin)
        self.__log("PIN changed")
        print("  ✅ PIN changed successfully.")

    def lock(self):
        self.__locked = True
        print(f"  🔒 Account for '{self.__owner}' locked.")

    def statement(self, pin):
        if not self.__verify_pin(pin):
            print("  ❌ Wrong PIN!")
            return
        print(f"\n  📋 Statement for {self.__owner}:")
        for t in self.__transactions:
            print(f"     {t}")
        print(f"  Current Balance: ₹{self.__balance}")

acc = BankAccount("Alice", 1234, 1000)
print(f"Owner: {acc.owner}  |  Balance: ₹{acc.balance}")
print(f"Interest Rate: {BankAccount.get_interest_rate()*100}%")
acc.deposit(500, 1234)
acc.withdraw(200, 1234)
acc.withdraw(200, 9999)    # wrong PIN
acc.change_pin(1234, 5678)
acc.deposit(300, 5678)     # new PIN works
acc.lock()
acc.deposit(100, 5678)     # blocked
acc.statement(5678)
