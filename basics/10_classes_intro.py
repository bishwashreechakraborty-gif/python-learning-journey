# 10_classes_intro.py — Introduction to Classes and Objects (OOP)

# ── Define a simple class ─────────────────
class Dog:
    # Constructor (runs when object is created)
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    # Method
    def bark(self):
        print(f"{self.name} says: Woof! 🐶")

    def info(self):
        print(f"Name: {self.name} | Breed: {self.breed} | Age: {self.age} years")

    def birthday(self):
        self.age += 1
        print(f"🎂 Happy Birthday {self.name}! Now {self.age} years old.")


# ── Create objects ────────────────────────
dog1 = Dog("Buddy", "Golden Retriever", 3)
dog2 = Dog("Max", "Labrador", 5)

dog1.info()
dog2.info()
dog1.bark()
dog2.bark()
dog1.birthday()

# ── Another class: BankAccount ────────────
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"  ✅ Deposited ₹{amount}. New balance: ₹{self.balance}")
        else:
            print("  ❌ Invalid deposit amount.")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"  ❌ Insufficient funds! Balance: ₹{self.balance}")
        elif amount <= 0:
            print("  ❌ Invalid amount.")
        else:
            self.balance -= amount
            print(f"  ✅ Withdrew ₹{amount}. New balance: ₹{self.balance}")

    def show_balance(self):
        print(f"  💰 {self.owner}'s Balance: ₹{self.balance}")


# ── Demo the BankAccount class ────────────
print("\n── Bank Account Demo ──")
acc = BankAccount("Alice", 1000)
acc.show_balance()
acc.deposit(500)
acc.withdraw(200)
acc.withdraw(2000)
acc.show_balance()

# ── Interactive account ───────────────────
print("\n── Your Account ──")
name = input("Enter your name: ")
my_acc = BankAccount(name)

while True:
    print("\n[1] Deposit  [2] Withdraw  [3] Balance  [4] Exit")
    choice = input("Choose: ").strip()
    if choice == "1":
        amt = float(input("Amount to deposit: ₹"))
        my_acc.deposit(amt)
    elif choice == "2":
        amt = float(input("Amount to withdraw: ₹"))
        my_acc.withdraw(amt)
    elif choice == "3":
        my_acc.show_balance()
    elif choice == "4":
        print("Goodbye! 👋")
        break
    else:
        print("Invalid choice.")
