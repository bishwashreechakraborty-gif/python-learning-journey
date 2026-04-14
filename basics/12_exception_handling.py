try:
    num = int(input("Enter a number: "))
    print("You entered:", num)
except ValueError:
    print("Invalid input! Please enter a number.")
finally:
    print("Program finished.")