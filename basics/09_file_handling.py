# 09_file_handling.py — Reading and Writing Files

import os

FILENAME = "notes.txt"

# ── Write to a file ───────────────────────
print("── Writing to file ──")
with open(FILENAME, "w") as f:
    f.write("Line 1: Hello from Python!\n")
    f.write("Line 2: File handling is easy.\n")
    f.write("Line 3: Reading and writing files.\n")
print(f"✅ Written to '{FILENAME}'")

# ── Append to a file ──────────────────────
with open(FILENAME, "a") as f:
    f.write("Line 4: This line was appended.\n")
print(f"✅ Appended to '{FILENAME}'")

# ── Read entire file ──────────────────────
print("\n── Reading entire file ──")
with open(FILENAME, "r") as f:
    content = f.read()
print(content)

# ── Read line by line ─────────────────────
print("── Reading line by line ──")
with open(FILENAME, "r") as f:
    for i, line in enumerate(f, 1):
        print(f"  {i}: {line.strip()}")

# ── Read all lines into a list ────────────
with open(FILENAME, "r") as f:
    lines = f.readlines()
print(f"\nTotal lines: {len(lines)}")

# ── Interactive: Let user write notes ─────
print("\n── Note Writer ──")
note_file = "my_notes.txt"
while True:
    note = input("Type a note (or 'done' to stop): ")
    if note.lower() == "done":
        break
    with open(note_file, "a") as f:
        f.write(note + "\n")
    print("  ✅ Note saved!")

# ── Show saved notes ──────────────────────
if os.path.exists(note_file):
    print(f"\n── Your Notes in '{note_file}' ──")
    with open(note_file, "r") as f:
        for i, line in enumerate(f, 1):
            print(f"  {i}. {line.strip()}")

# ── Check if file exists ──────────────────
for fname in [FILENAME, note_file, "missing.txt"]:
    exists = os.path.exists(fname)
    print(f"  '{fname}' exists: {exists}")
