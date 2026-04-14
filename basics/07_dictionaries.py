# 07_dictionaries.py — Working with Dictionaries (key-value pairs)

# ── Create a dictionary ───────────────────
student = {
    "name": "Alice",
    "age": 20,
    "grade": "A",
    "subject": "Python"
}
print("Student Info:", student)

# ── Access values ─────────────────────────
print("\nName:", student["name"])
print("Age:", student.get("age"))       # .get() is safe (no error if key missing)
print("Score:", student.get("score", "Not found"))

# ── Update and add keys ───────────────────
student["age"] = 21                     # Update
student["score"] = 95                   # Add new key
print("\nUpdated student:", student)

# ── Remove a key ─────────────────────────
student.pop("subject")
print("After removing 'subject':", student)

# ── Loop through dictionary ───────────────
print("\n── All Student Details ──")
for key, value in student.items():
    print(f"  {key}: {value}")

# ── Practical: Simple phonebook ──────────
phonebook = {
    "Alice": "9876543210",
    "Bob": "9123456789",
    "Carol": "9988776655"
}

print("\n── Phonebook ──")
for name, number in phonebook.items():
    print(f"  {name}: {number}")

search = input("\nSearch for a contact: ")
if search in phonebook:
    print(f"📞 {search}'s number: {phonebook[search]}")
else:
    print("❌ Contact not found.")

# ── Word frequency counter ────────────────
sentence = input("\nEnter a sentence: ").lower().split()
word_count = {}

for word in sentence:
    word_count[word] = word_count.get(word, 0) + 1

print("\n── Word Frequencies ──")
for word, count in sorted(word_count.items()):
    print(f"  '{word}': {count}")
