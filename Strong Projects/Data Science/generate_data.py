"""
generate_data.py — Creates sample CSV datasets for analysis.
Run this FIRST before running analysis.py
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# ── 1. Student Performance Dataset ──────────────────────
students = []
names = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Hank",
         "Iris", "Jack", "Karen", "Leo", "Mia", "Noah", "Olivia", "Peter",
         "Quinn", "Rosa", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xander",
         "Yara", "Zoe", "Arjun", "Priya", "Rahul", "Sneha"]
courses  = ["Computer Science", "Mathematics", "Physics", "Commerce", "Biology"]
sections = ["A", "B", "C"]
genders  = ["Male", "Female"]

for i, name in enumerate(names):
    course  = random.choice(courses)
    gender  = random.choice(genders)
    section = random.choice(sections)
    # Generate correlated marks
    base = random.randint(40, 95)
    students.append({
        "student_id": f"STU{i+1:03d}",
        "name":       name,
        "gender":     gender,
        "course":     course,
        "section":    section,
        "math":       min(100, max(0, base + random.randint(-15, 15))),
        "science":    min(100, max(0, base + random.randint(-20, 10))),
        "english":    min(100, max(0, base + random.randint(-10, 20))),
        "history":    min(100, max(0, base + random.randint(-25, 15))),
        "computer":   min(100, max(0, base + random.randint(-5,  25))),
        "attendance": round(random.uniform(60, 100), 1),
    })

with open("data/students.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=students[0].keys())
    writer.writeheader()
    writer.writerows(students)

print(f"✅ data/students.csv — {len(students)} students")


# ── 2. Sales Dataset ─────────────────────────────────────
sales = []
products = ["Laptop", "Phone", "Tablet", "Headphones", "Keyboard",
            "Mouse", "Monitor", "Webcam", "Speaker", "Charger"]
regions  = ["North", "South", "East", "West"]
prices   = {"Laptop": 55000, "Phone": 25000, "Tablet": 18000,
            "Headphones": 3000, "Keyboard": 1500, "Mouse": 800,
            "Monitor": 15000, "Webcam": 2500, "Speaker": 4000, "Charger": 600}

start_date = datetime(2024, 1, 1)
for i in range(500):
    product  = random.choice(products)
    region   = random.choice(regions)
    quantity = random.randint(1, 20)
    price    = prices[product] * random.uniform(0.85, 1.15)
    discount = random.choice([0, 5, 10, 15, 20])
    revenue  = round(quantity * price * (1 - discount/100), 2)
    sale_date = (start_date + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
    sales.append({
        "sale_id":  f"S{i+1:04d}",
        "date":     sale_date,
        "product":  product,
        "region":   region,
        "quantity": quantity,
        "unit_price": round(price, 2),
        "discount":  discount,
        "revenue":   revenue,
    })

with open("data/sales.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=sales[0].keys())
    writer.writeheader()
    writer.writerows(sales)

print(f"✅ data/sales.csv — {len(sales)} records")
print("\nNow run: python analysis.py")
