# ============================================================
#  PHASE 2 — Topic 3: File Handling
#  Covers: read, write, append, CSV, JSON, os operations
# ============================================================

import os
import csv
import json

# ── 1. Write a file ───────────────────────────────────────
print("=== 1. Writing a Text File ===")
with open("sample.txt", "w") as f:
    f.write("Line 1: Python file handling\n")
    f.write("Line 2: Read, Write, Append\n")
    f.write("Line 3: Always use 'with' statement\n")
print("✅ sample.txt created")


# ── 2. Read entire file ───────────────────────────────────
print("\n=== 2. Reading Entire File ===")
with open("sample.txt", "r") as f:
    content = f.read()
print(content)


# ── 3. Read line by line ──────────────────────────────────
print("=== 3. Reading Line by Line ===")
with open("sample.txt", "r") as f:
    for line_num, line in enumerate(f, 1):
        print(f"  [{line_num}] {line.strip()}")


# ── 4. Read all lines into a list ────────────────────────
with open("sample.txt", "r") as f:
    lines = f.readlines()
print(f"\nTotal lines: {len(lines)}")
print("First line:", lines[0].strip())
print("Last line:", lines[-1].strip())


# ── 5. Append to a file ───────────────────────────────────
print("\n=== 5. Appending to File ===")
with open("sample.txt", "a") as f:
    f.write("Line 4: This line was appended later.\n")
print("✅ Appended successfully")

# Confirm
with open("sample.txt", "r") as f:
    print("File now has", len(f.readlines()), "lines")


# ── 6. Check if file exists before reading ───────────────
print("\n=== 6. Safe File Reading ===")
for fname in ["sample.txt", "missing.txt"]:
    if os.path.exists(fname):
        with open(fname, "r") as f:
            data = f.read()
        print(f"✅ Read '{fname}': {len(data)} characters")
    else:
        print(f"❌ '{fname}' does not exist")


# ── 7. File modes summary ─────────────────────────────────
print("\n=== 7. File Modes ===")
modes = {
    "'r'":  "Read only (default) — error if file doesn't exist",
    "'w'":  "Write — creates new OR overwrites existing file",
    "'a'":  "Append — adds to end, creates if not exists",
    "'r+'": "Read and write — file must exist",
    "'x'":  "Create — error if file already exists",
    "'rb'": "Read binary (images, PDFs, etc.)",
    "'wb'": "Write binary",
}
for mode, desc in modes.items():
    print(f"  {mode:<6} → {desc}")


# ── 8. Working with CSV files ─────────────────────────────
print("\n=== 8. CSV File Handling ===")

# Write CSV
students = [
    ["Name", "Age", "Grade"],
    ["Alice", 20, "A"],
    ["Bob", 22, "B"],
    ["Carol", 21, "A"],
    ["David", 23, "C"],
]
with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)
print("✅ students.csv created")

# Read CSV
print("\nReading students.csv:")
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['Name']:<10} Age: {row['Age']}  Grade: {row['Grade']}")


# ── 9. Working with JSON files ───────────────────────────
print("\n=== 9. JSON File Handling ===")

profile = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "SQL", "HTML"],
    "address": {"city": "Delhi", "country": "India"}
}

# Write JSON
with open("profile.json", "w") as f:
    json.dump(profile, f, indent=4)
print("✅ profile.json created")

# Read JSON
with open("profile.json", "r") as f:
    loaded = json.load(f)
print("Name:", loaded["name"])
print("Skills:", ", ".join(loaded["skills"]))
print("City:", loaded["address"]["city"])


# ── 10. OS file operations ───────────────────────────────
print("\n=== 10. OS File Operations ===")

# Rename a file
os.rename("sample.txt", "renamed_sample.txt")
print("✅ Renamed sample.txt → renamed_sample.txt")

# Get file size
size = os.path.getsize("renamed_sample.txt")
print(f"File size: {size} bytes")

# List files in current directory
txt_files = [f for f in os.listdir(".") if f.endswith(".txt")]
print("Text files in folder:", txt_files)

# Create and remove a directory
os.makedirs("temp_folder", exist_ok=True)
print("✅ Created temp_folder/")
os.rmdir("temp_folder")
print("✅ Removed temp_folder/")

# Clean up demo files
for f in ["renamed_sample.txt", "students.csv", "profile.json", "sample_data.json"]:
    if os.path.exists(f):
        os.remove(f)
print("✅ Cleaned up demo files")
