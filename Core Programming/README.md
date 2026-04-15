# 🐍 Core Programming — Python

> **Goal:** Write structured and reusable code

---

## 📁 Folder Structure

```
phase2_core_programming/
│
├── topics/
│   ├── 01_functions.py              ← Arguments, return, *args, recursion
│   ├── 02_modules_and_packages.py   ← math, random, datetime, os, json
│   ├── 03_file_handling.py          ← Read, write, CSV, JSON, os ops
│   └── 04_exception_handling.py     ← try/except, raise, custom exceptions
│
├── projects/
│   ├── project1_calculator.py       ← Full calculator with history & file save
│   ├── project2_notes_app.py        ← File-based notes (add/edit/delete/search)
│   └── project3_password_checker.py ← Password strength + generator
│
└── README.md
```

---

## 📚 Topics Covered

| File | Topic | Key Concepts |
|------|-------|-------------|
| `01_functions.py` | Functions | positional, default, `*args`, `**kwargs`, lambda, recursion, scope |
| `02_modules_and_packages.py` | Modules & Packages | math, random, datetime, os, sys, json, custom modules |
| `03_file_handling.py` | File Handling | read, write, append, CSV, JSON, os file operations |
| `04_exception_handling.py` | Exception Handling | try/except/else/finally, raise, custom exceptions |

---

## 🚀 Projects

### 🧮 Project 1 — Calculator
- All basic operations: +, −, ×, ÷, %, power, √, log
- Calculation history stored in memory and saved to file
- Input validation with exception handling
- Clean menu-driven interface

### 📓 Project 2 — File-Based Notes App
- Add, view, read, search, edit, delete notes
- All notes saved to `notes_data.json` (persistent across runs)
- Export notes to a `.txt` file with timestamp
- Timestamps for created/updated on each note

### 🔐 Project 3 — Password Checker & Generator
- Checks: length, uppercase, lowercase, digits, symbols, sequences
- Strength score (0–10) with grade (A+ to F) and visual bar
- Lists specific improvements for weak passwords
- Generates secure random passwords with custom options
- Saves check history to `password_history.json`

---

## ▶️ How to Run

```bash
# Run any topic file
python topics/01_functions.py

# Run a project
python projects/project1_calculator.py
python projects/project2_notes_app.py
python projects/project3_password_checker.py
```

Or open the folder in **VS Code** and click the **▷ Run** button.

---

## 💡 Tips

- Read the comments in each file — every concept is explained!
- Topics teach the concept; Projects apply multiple topics together
- Python 3.7+ required | No external packages needed

### Developed by Bishwashree Chakraborty