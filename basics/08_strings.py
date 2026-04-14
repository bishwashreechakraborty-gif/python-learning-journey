# 08_strings.py — Common String Methods and Operations

text = "  Hello, Python World!  "

# ── Basic operations ──────────────────────
print("Original  :", repr(text))
print("Strip     :", text.strip())           # Remove spaces
print("Upper     :", text.strip().upper())
print("Lower     :", text.strip().lower())
print("Title     :", text.strip().title())   # Capitalize each word
print("Length    :", len(text.strip()))

# ── Search and replace ────────────────────
sentence = "I love Python. Python is great."
print("\nOriginal :", sentence)
print("Replace  :", sentence.replace("Python", "coding"))
print("Find 'Python' at index:", sentence.find("Python"))
print("Count 'Python':", sentence.count("Python"))
print("Starts with 'I':", sentence.startswith("I"))
print("Ends with '.':", sentence.endswith("."))

# ── Split and join ────────────────────────
csv_line = "apple,banana,cherry,mango"
items = csv_line.split(",")
print("\nSplit:", items)

joined = " | ".join(items)
print("Joined:", joined)

# ── String formatting ─────────────────────
name = "Alice"
score = 95.678
print("\n── Formatting ──")
print(f"Name: {name}, Score: {score}")
print(f"Score rounded: {score:.2f}")
print(f"Right-aligned: {name:>15}")
print(f"Left-aligned:  {name:<15}|")
print(f"Padded number: {42:05d}")

# ── Check string type ─────────────────────
samples = ["Hello123", "12345", "HelloWorld", "hello world", "HELLO"]
print("\n── String Checks ──")
for s in samples:
    print(f"  '{s}'  isalpha={s.isalpha():<5}  isdigit={s.isdigit():<5}  "
          f"isupper={s.isupper():<5}  islower={s.islower()}")

# ── Reverse a string ─────────────────────
word = input("\nEnter a word to reverse: ")
print("Reversed:", word[::-1])

# ── Palindrome checker ────────────────────
cleaned = word.lower().replace(" ", "")
if cleaned == cleaned[::-1]:
    print(f"'{word}' IS a palindrome! ✅")
else:
    print(f"'{word}' is NOT a palindrome. ❌")
