def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("1. Add\n2. Subtract")
choice = input("Choose operation: ")

if choice == "1":
    print("Result:", add(a, b))
elif choice == "2":
    print("Result:", subtract(a, b))
else:
    print("Invalid choice")