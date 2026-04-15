# ============================================================
#  Project 2: Bank Account System
#  OOP Concepts: Inheritance, Encapsulation, Polymorphism,
#                @property, Abstract classes, JSON persistence
# ============================================================

import json, os, random
from datetime import datetime
from abc import ABC, abstractmethod

DATA_FILE = "bank_db.json"

# ────────────────────────────────────────────────────────────
#  TRANSACTION
# ────────────────────────────────────────────────────────────

class Transaction:
    def __init__(self, txn_type, amount, balance_after, note=""):
        self.txn_type      = txn_type
        self.amount        = amount
        self.balance_after = balance_after
        self.note          = note
        self.timestamp     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        sign = "+" if self.txn_type in ("Deposit", "Interest") else "-"
        return (f"  {self.timestamp}  {self.txn_type:<12} "
                f"{sign}₹{self.amount:<10.2f}  Bal: ₹{self.balance_after:.2f}"
                + (f"  [{self.note}]" if self.note else ""))

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(d):
        t = Transaction.__new__(Transaction)
        t.__dict__.update(d)
        return t


# ────────────────────────────────────────────────────────────
#  BASE ACCOUNT (Abstract)
# ────────────────────────────────────────────────────────────

class Account(ABC):
    _acc_counter = 1000

    def __init__(self, owner, pin, initial=0):
        self._acc_no       = f"ACC{Account._acc_counter:05d}"
        self._owner        = owner
        self.__pin         = str(pin)
        self._balance      = float(initial)
        self._transactions = []
        self._created      = datetime.now().strftime("%Y-%m-%d")
        self._active       = True
        Account._acc_counter += 1

    # ── PIN ───────────────────────────────────────────────
    def _verify(self, pin):
        return str(pin) == self.__pin

    def change_pin(self, old, new):
        if not self._verify(old):
            print("  ❌ Wrong PIN.")
            return False
        self.__pin = str(new)
        print("  ✅ PIN changed.")
        return True

    # ── Properties ────────────────────────────────────────
    @property
    def acc_no(self):  return self._acc_no
    @property
    def owner(self):   return self._owner
    @property
    def balance(self): return self._balance
    @property
    def active(self):  return self._active

    # ── Core operations ───────────────────────────────────
    def deposit(self, amount, pin, note=""):
        if not self._active:   return print("  🔒 Account inactive.")
        if not self._verify(pin): return print("  ❌ Wrong PIN.")
        if amount <= 0:        return print("  ❌ Invalid amount.")
        self._balance += amount
        self._log("Deposit", amount, note)
        print(f"  ✅ Deposited ₹{amount:.2f}. Balance: ₹{self._balance:.2f}")

    def withdraw(self, amount, pin, note=""):
        if not self._active:   return print("  🔒 Account inactive.")
        if not self._verify(pin): return print("  ❌ Wrong PIN.")
        if amount <= 0:        return print("  ❌ Invalid amount.")
        if amount > self._balance:
            return print(f"  ❌ Insufficient funds. Balance: ₹{self._balance:.2f}")
        self._balance -= amount
        self._log("Withdrawal", amount, note)
        print(f"  ✅ Withdrew ₹{amount:.2f}. Balance: ₹{self._balance:.2f}")

    def transfer(self, amount, pin, target_account):
        if not self._active:   return print("  🔒 Account inactive.")
        if not self._verify(pin): return print("  ❌ Wrong PIN.")
        if amount > self._balance:
            return print(f"  ❌ Insufficient funds.")
        self._balance -= amount
        target_account._balance += amount
        self._log("Transfer Out", amount, f"To: {target_account.acc_no}")
        target_account._log("Transfer In", amount, f"From: {self._acc_no}")
        print(f"  ✅ ₹{amount:.2f} transferred to {target_account.acc_no}")

    def _log(self, txn_type, amount, note=""):
        self._transactions.append(
            Transaction(txn_type, amount, self._balance, note)
        )

    def statement(self, pin, last_n=10):
        if not self._verify(pin): return print("  ❌ Wrong PIN.")
        print(f"\n  {'═'*65}")
        print(f"  Account: {self._acc_no}  |  Owner: {self._owner}  "
              f"|  Type: {self.__class__.__name__}")
        print(f"  {'─'*65}")
        recent = self._transactions[-last_n:]
        if not recent:
            print("  No transactions yet.")
        for t in recent:
            print(t)
        print(f"  {'─'*65}")
        print(f"  Current Balance: ₹{self._balance:.2f}")
        print(f"  {'═'*65}")

    def close(self, pin):
        if not self._verify(pin): return print("  ❌ Wrong PIN.")
        self._active = False
        print(f"  🔒 Account {self._acc_no} closed.")

    @abstractmethod
    def account_type(self): pass

    @abstractmethod
    def apply_interest(self): pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "acc_no": self._acc_no,
            "owner": self._owner,
            "pin": self.__pin,
            "balance": self._balance,
            "created": self._created,
            "active": self._active,
            "transactions": [t.to_dict() for t in self._transactions],
            **self._extra_dict(),
        }

    def _extra_dict(self): return {}

    @classmethod
    def _base_restore(cls, obj, d):
        obj._acc_no       = d["acc_no"]
        obj._owner        = d["owner"]
        obj._Account__pin = d["pin"]
        obj._balance      = d["balance"]
        obj._created      = d["created"]
        obj._active       = d["active"]
        obj._transactions = [Transaction.from_dict(t) for t in d.get("transactions", [])]

    def __str__(self):
        status = "✅ Active" if self._active else "🔒 Closed"
        return (f"[{self._acc_no}] {self._owner:<15} "
                f"{self.account_type():<18} ₹{self._balance:>10.2f}  {status}")


# ────────────────────────────────────────────────────────────
#  ACCOUNT TYPES (Inheritance + Polymorphism)
# ────────────────────────────────────────────────────────────

class SavingsAccount(Account):
    INTEREST_RATE = 0.04   # 4% per year

    def __init__(self, owner, pin, initial=0):
        super().__init__(owner, pin, initial)
        self.__interest_earned = 0.0

    def account_type(self): return "Savings Account"

    def apply_interest(self):
        interest = round(self._balance * self.INTEREST_RATE, 2)
        self._balance += interest
        self.__interest_earned += interest
        self._log("Interest", interest, f"{self.INTEREST_RATE*100}% annual")
        print(f"  💰 Interest ₹{interest:.2f} credited. Balance: ₹{self._balance:.2f}")

    def _extra_dict(self):
        return {"interest_earned": self.__interest_earned}

    @classmethod
    def from_dict(cls, d):
        obj = cls.__new__(cls)
        cls._base_restore(obj, d)
        obj._SavingsAccount__interest_earned = d.get("interest_earned", 0)
        return obj


class CurrentAccount(Account):
    OVERDRAFT_LIMIT = 10000

    def account_type(self): return "Current Account"

    def withdraw(self, amount, pin, note=""):
        if not self._active:   return print("  🔒 Account inactive.")
        if not self._verify(pin): return print("  ❌ Wrong PIN.")
        if amount > self._balance + self.OVERDRAFT_LIMIT:
            return print(f"  ❌ Exceeds overdraft limit ₹{self.OVERDRAFT_LIMIT}")
        self._balance -= amount
        self._log("Withdrawal", amount, note)
        bal_str = f"₹{self._balance:.2f}" + (" (overdraft)" if self._balance < 0 else "")
        print(f"  ✅ Withdrew ₹{amount:.2f}. Balance: {bal_str}")

    def apply_interest(self):
        print("  ℹ️  No interest on Current Accounts.")

    @classmethod
    def from_dict(cls, d):
        obj = cls.__new__(cls)
        cls._base_restore(obj, d)
        return obj


class FixedDepositAccount(Account):
    INTEREST_RATE = 0.075  # 7.5%

    def __init__(self, owner, pin, amount, tenure_years):
        super().__init__(owner, pin, amount)
        self.__tenure   = tenure_years
        self.__maturity = amount * (1 + self.INTEREST_RATE) ** tenure_years

    def account_type(self): return "Fixed Deposit"

    def withdraw(self, amount, pin, note=""):
        print("  ⚠️  FD accounts cannot be partially withdrawn before maturity.")

    def apply_interest(self):
        print(f"  📈 FD matures at ₹{self.__maturity:.2f} after {self.__tenure} year(s)")

    def _extra_dict(self):
        return {"tenure": self.__tenure, "maturity": self.__maturity}

    @classmethod
    def from_dict(cls, d):
        obj = cls.__new__(cls)
        cls._base_restore(obj, d)
        obj._FixedDepositAccount__tenure   = d.get("tenure", 1)
        obj._FixedDepositAccount__maturity = d.get("maturity", 0)
        return obj


# ────────────────────────────────────────────────────────────
#  BANK SYSTEM
# ────────────────────────────────────────────────────────────

class Bank:
    def __init__(self, name="PyBank"):
        self.name = name
        self.__accounts = {}
        self.__load()

    def __load(self):
        if not os.path.exists(DATA_FILE): return
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
            loaders = {"SavingsAccount": SavingsAccount,
                       "CurrentAccount": CurrentAccount,
                       "FixedDepositAccount": FixedDepositAccount}
            for d in data:
                cls = loaders.get(d["type"])
                if cls:
                    acc = cls.from_dict(d)
                    self.__accounts[acc.acc_no] = acc
            if self.__accounts:
                max_no = max(int(k[3:]) for k in self.__accounts)
                Account._acc_counter = max_no + 1
            print(f"  📂 Loaded {len(self.__accounts)} account(s).")
        except Exception as e:
            print(f"  ⚠️  Load error: {e}")

    def __save(self):
        with open(DATA_FILE, "w") as f:
            json.dump([a.to_dict() for a in self.__accounts.values()], f, indent=2)

    def __get(self, acc_no):
        acc = self.__accounts.get(acc_no.upper())
        if not acc: print("  ❌ Account not found.")
        return acc

    # ── Account creation ──────────────────────────────────
    def open_savings(self):
        print("\n── Open Savings Account ─────────────")
        owner   = input("  Name    : ")
        pin     = input("  Set PIN : ")
        initial = float(input("  Initial Deposit (₹): ") or 0)
        acc = SavingsAccount(owner, pin, initial)
        self.__accounts[acc.acc_no] = acc
        self.__save()
        print(f"  ✅ Account opened! ID: {acc.acc_no}")

    def open_current(self):
        print("\n── Open Current Account ─────────────")
        owner = input("  Name    : ")
        pin   = input("  Set PIN : ")
        acc = CurrentAccount(owner, pin)
        self.__accounts[acc.acc_no] = acc
        self.__save()
        print(f"  ✅ Account opened! ID: {acc.acc_no}")

    def open_fd(self):
        print("\n── Open Fixed Deposit ───────────────")
        owner   = input("  Name        : ")
        pin     = input("  Set PIN     : ")
        amount  = float(input("  FD Amount (₹): "))
        tenure  = int(input("  Tenure (yrs) : "))
        acc = FixedDepositAccount(owner, pin, amount, tenure)
        self.__accounts[acc.acc_no] = acc
        self.__save()
        print(f"  ✅ FD opened! ID: {acc.acc_no}")

    # ── Operations ────────────────────────────────────────
    def deposit(self):
        acc_no = input("\n  Account No: ").upper()
        acc = self.__get(acc_no)
        if not acc: return
        amount = float(input("  Amount (₹): "))
        pin    = input("  PIN       : ")
        note   = input("  Note (optional): ")
        acc.deposit(amount, pin, note)
        self.__save()

    def withdraw(self):
        acc_no = input("\n  Account No: ").upper()
        acc = self.__get(acc_no)
        if not acc: return
        amount = float(input("  Amount (₹): "))
        pin    = input("  PIN       : ")
        acc.withdraw(amount, pin)
        self.__save()

    def transfer(self):
        from_no = input("\n  From Account: ").upper()
        to_no   = input("  To   Account: ").upper()
        src = self.__get(from_no)
        dst = self.__get(to_no)
        if not src or not dst: return
        amount = float(input("  Amount (₹): "))
        pin    = input("  PIN       : ")
        src.transfer(amount, pin, dst)
        self.__save()

    def statement(self):
        acc_no = input("\n  Account No: ").upper()
        acc = self.__get(acc_no)
        if not acc: return
        pin = input("  PIN: ")
        acc.statement(pin)

    def apply_all_interest(self):
        print("\n  Applying interest to all accounts...")
        for acc in self.__accounts.values():
            if acc.active:
                print(f"  {acc.acc_no} ({acc.owner}):")
                acc.apply_interest()
        self.__save()

    def list_accounts(self):
        print(f"\n  {'═'*60}")
        print(f"  {'Account No':<12} {'Owner':<16} {'Type':<20} {'Balance':>12}  Status")
        print(f"  {'─'*60}")
        for acc in self.__accounts.values():
            print(f"  {acc}")
        print(f"  {'═'*60}")
        print(f"  Total accounts: {len(self.__accounts)}")
        total = sum(a.balance for a in self.__accounts.values() if a.active)
        print(f"  Total deposits: ₹{total:.2f}")

    def run(self):
        print(f"\n  Welcome to {self.name} 🏦")
        options = [
            ("1",  "Open Savings Account",   self.open_savings),
            ("2",  "Open Current Account",   self.open_current),
            ("3",  "Open Fixed Deposit",     self.open_fd),
            ("4",  "Deposit",                self.deposit),
            ("5",  "Withdraw",               self.withdraw),
            ("6",  "Transfer",               self.transfer),
            ("7",  "Mini Statement",         self.statement),
            ("8",  "All Accounts",           self.list_accounts),
            ("9",  "Apply Interest (All)",   self.apply_all_interest),
            ("0",  "Exit",                   None),
        ]
        while True:
            print(f"\n{'═'*35}")
            print(f"  🏦  {self.name}")
            print(f"{'─'*35}")
            for key, label, _ in options:
                print(f"  [{key}] {label}")
            choice = input("  Choice: ").strip()
            if choice == "0":
                print("\n  Thank you for banking with us! 👋")
                break
            match = next(((k,l,fn) for k,l,fn in options if k == choice), None)
            if match:
                try:
                    match[2]()
                except ValueError as e:
                    print(f"  ❌ {e}")
            else:
                print("  ⚠️  Invalid choice.")

if __name__ == "__main__":
    Bank("PyBank 🏦").run()
