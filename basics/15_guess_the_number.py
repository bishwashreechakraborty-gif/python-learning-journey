import random

secret = random.randint(1, 10)

while True:
    guess = int(input("Guess the number (1-10): "))
    
    if guess == secret:
        print("Correct! 🎉")
        break
    elif guess < secret:
        print("Too low!")
    else:
        print("Too high!")