# ============================================================
#  Topic 1: Classes & Objects
#  Covers: class definition, attributes, methods, __str__,
#          class variables vs instance variables, @classmethod
# ============================================================

# ── 1. Defining a basic class ─────────────────────────────
class Dog:
    # Class variable (shared by ALL instances)
    species = "Canis lupus familiaris"
    count = 0

    # Constructor (instance variables — unique per object)
    def __init__(self, name, breed, age):
        self.name  = name
        self.breed = breed
        self.age   = age
        Dog.count += 1          # track total dogs created

    # Instance methods
    def bark(self):
        return f"{self.name} says: Woof! 🐶"

    def describe(self):
        return f"{self.name} is a {self.age}-year-old {self.breed}."

    # __str__: controls what print(dog) shows
    def __str__(self):
        return f"Dog({self.name}, {self.breed}, {self.age})"

    # __repr__: developer-friendly representation
    def __repr__(self):
        return f"Dog(name='{self.name}', breed='{self.breed}', age={self.age})"

    # Class method — works on the class, not an instance
    @classmethod
    def total_dogs(cls):
        return f"Total dogs created: {cls.count}"

    # Static method — utility, no self or cls needed
    @staticmethod
    def is_adult(age):
        return age >= 2


# ── Creating objects (instances) ─────────────────────────
dog1 = Dog("Buddy", "Golden Retriever", 3)
dog2 = Dog("Max",   "Labrador",         5)
dog3 = Dog("Luna",  "Poodle",           1)

print(dog1)                      # uses __str__
print(repr(dog2))                # uses __repr__
print(dog1.bark())
print(dog2.describe())
print(Dog.total_dogs())
print("Buddy adult?", Dog.is_adult(dog1.age))
print("Luna adult?",  Dog.is_adult(dog3.age))
print("Species:", dog1.species)  # class variable via instance


# ── 2. Class with validation ──────────────────────────────
print("\n" + "="*50)
print("  Rectangle Class")
print("="*50)

class Rectangle:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self.width  = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

    def scale(self, factor):
        """Return a new Rectangle scaled by factor."""
        return Rectangle(self.width * factor, self.height * factor)

    def __str__(self):
        return f"Rectangle({self.width} × {self.height})"

    # Comparison operators
    def __eq__(self, other):
        return self.area() == other.area()

    def __lt__(self, other):
        return self.area() < other.area()


r1 = Rectangle(4, 6)
r2 = Rectangle(5, 5)
r3 = r1.scale(2)

print(r1, "→ area:", r1.area(), "| perimeter:", r1.perimeter())
print(r2, "→ is square:", r2.is_square())
print(r3, "← scaled r1 × 2")
print(f"r1 == r2? {r1 == r2}")
print(f"r1 <  r2? {r1 < r2}")


# ── 3. Object interaction ─────────────────────────────────
print("\n" + "="*50)
print("  Simple Shopping Cart")
print("="*50)

class Product:
    def __init__(self, name, price, stock):
        self.name  = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} (₹{self.price}) — stock: {self.stock}"

class Cart:
    def __init__(self):
        self.items = []     # list of (Product, quantity) tuples

    def add(self, product, qty=1):
        if qty > product.stock:
            print(f"  ❌ Not enough stock for {product.name}")
            return
        self.items.append((product, qty))
        product.stock -= qty
        print(f"  ✅ Added {qty}× {product.name}")

    def total(self):
        return sum(p.price * q for p, q in self.items)

    def show(self):
        print("\n  🛒 Cart:")
        for product, qty in self.items:
            print(f"    {product.name:<15} ×{qty}  ₹{product.price * qty}")
        print(f"  {'─'*30}")
        print(f"  Total: ₹{self.total()}")


p1 = Product("Python Book",   499, 10)
p2 = Product("USB Cable",     199,  3)
p3 = Product("Laptop Stand", 1299,  1)

cart = Cart()
cart.add(p1, 2)
cart.add(p2, 1)
cart.add(p3, 1)
cart.add(p3, 1)    # should fail — out of stock
cart.show()
