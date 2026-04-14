numbers = [1, 2, 3, 4]

# lambda
square = lambda x: x**2
print(square(5))

# map
squares = list(map(lambda x: x**2, numbers))
print(squares)

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)