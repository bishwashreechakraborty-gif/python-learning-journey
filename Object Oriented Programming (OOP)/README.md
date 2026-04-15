# 🧠 Object-Oriented Programming (OOP)

> **Goal:** Think like a software developer

---

## 📁 Folder Structure

```
OOP/
├── topics/
│   ├── 01_classes_and_objects.py     ← Class, instance vars, @classmethod, @staticmethod
│   ├── 02_constructors.py            ← __init__, defaults, @classmethod constructors, __del__
│   ├── 03_inheritance.py             ← Single, multi-level, multiple, super(), ABC
│   ├── 04_polymorphism.py            ← Method overriding, duck typing, operator overloading
│   └── 05_encapsulation.py           ← Public/protected/private, @property, getters/setters
│
└── projects/
    ├── project1_student_management.py  ← Full CRUD student system with JSON storage
    ├── project2_bank_account.py        ← 3 account types (Savings/Current/FD), transfers
    └── project3_library_management.py  ← Books/Magazines/DVDs, members, fines, borrowing
```

---

## 📚 Topics

| File | Concepts |
|------|----------|
| `01_classes_and_objects.py` | class, `__init__`, `__str__`, `__repr__`, `@classmethod`, `@staticmethod` |
| `02_constructors.py` | default params, mutable defaults, alternative constructors, `__del__`, deep copy |
| `03_inheritance.py` | `super()`, multi-level, multiple inheritance, MRO, Abstract Base Classes (`abc`) |
| `04_polymorphism.py` | method overriding, duck typing, operator overloading (`__add__`, `__eq__`, etc.) |
| `05_encapsulation.py` | `_protected`, `__private`, `@property`, getter/setter, name mangling |

---

## 🚀 Projects

### 🎓 Project 1 — Student Management System
- Add, view, search, delete students
- Add grades per subject → auto-calculate average & letter grade
- Printable report card
- Saved to `students_db.json`

### 🏦 Project 2 — Bank Account System
- **3 account types**: Savings (4% interest), Current (overdraft), Fixed Deposit (7.5%)
- Deposit, Withdraw, Transfer between accounts
- PIN authentication, account locking
- Saved to `bank_db.json`

### 📚 Project 3 — Library Management System
- **3 item types**: Books, Magazines, DVDs (each with different borrow periods)
- Register members, borrow/return items
- Auto-calculate overdue fines (₹5/day)
- Pay fines, export statistics
- Saved to `library_db.json`

---

## ▶️ How to Run

```bash
python topics/01_classes_and_objects.py
python projects/project1_student_management.py
```

**Python 3.7+ | No external packages needed**


### Developed by Bishwashree Chakraborty