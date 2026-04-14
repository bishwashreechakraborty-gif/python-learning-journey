# 05_lists.py — Working with Lists

# ── Create a list ─────────────────────────
fruits = ["apple", "banana", "cherry", "mango", "grape"]
print("Fruits:", fruits)

# ── Access items ──────────────────────────
print("\nFirst fruit:", fruits[0])
print("Last fruit:", fruits[-1])
print("Second to fourth:", fruits[1:4])

# ── Change an item ────────────────────────
fruits[1] = "blueberry"
print("\nAfter changing index 1:", fruits)

# ── Add items ─────────────────────────────
fruits.append("orange")          # Add to end
fruits.insert(2, "kiwi")         # Insert at position
print("After adding items:", fruits)

# ── Remove items ──────────────────────────
fruits.remove("grape")           # Remove by value
popped = fruits.pop()            # Remove last item
print("After removing 'grape' and last item:", fruits)
print("Popped item:", popped)

# ── List info ─────────────────────────────
numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]
print("\nNumbers:", numbers)
print("Length:", len(numbers))
print("Max:", max(numbers))
print("Min:", min(numbers))
print("Sum:", sum(numbers))

# ── Sort a list ───────────────────────────
numbers.sort()
print("Sorted:", numbers)
numbers.sort(reverse=True)
print("Reverse sorted:", numbers)

# ── Check if item exists ──────────────────
item = input("\nEnter a fruit to search: ")
if item in fruits:
    print(f"✅ '{item}' is in the list!")
else:
    print(f"❌ '{item}' is NOT in the list.")

# ── Loop through list with index ──────────
print("\n── Fruits with Index ──")
for index, fruit in enumerate(fruits):
    print(f"  [{index}] {fruit}")

# ── List comprehension ────────────────────
squares = [x ** 2 for x in range(1, 6)]
print("\nSquares of 1-5:", squares)

evens = [x for x in range(1, 21) if x % 2 == 0]
print("Even numbers 1-20:", evens)
