# ============================================================
#  Topic 3: Inheritance
#  Covers: single, multi-level, multiple inheritance,
#          super(), method overriding, isinstance/issubclass
# ============================================================

# ── 1. Single Inheritance ─────────────────────────────────
print("=== 1. Single Inheritance ===")

class Animal:
    def __init__(self, name, sound):
        self.name  = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}!"

    def breathe(self):
        return f"{self.name} breathes air."

    def __str__(self):
        return f"Animal: {self.name}"

class Dog(Animal):               # Dog inherits from Animal
    def __init__(self, name, breed):
        super().__init__(name, "Woof")   # call parent __init__
        self.breed = breed

    def fetch(self):
        return f"{self.name} fetches the ball! 🎾"

    def __str__(self):
        return f"Dog: {self.name} ({self.breed})"

class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, "Meow")
        self.indoor = indoor

    def purr(self):
        return f"{self.name} purrs... 😸"

dog = Dog("Buddy", "Labrador")
cat = Cat("Whiskers")

print(dog)
print(dog.speak())        # inherited from Animal
print(dog.breathe())      # inherited from Animal
print(dog.fetch())        # Dog's own method
print(cat.speak())
print(cat.purr())


# ── 2. Multi-level Inheritance ────────────────────────────
print("\n=== 2. Multi-level Inheritance ===")

class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def move(self):
        return f"{self.brand} moves at {self.speed} km/h"

class Car(Vehicle):
    def __init__(self, brand, speed, doors):
        super().__init__(brand, speed)
        self.doors = doors

    def honk(self):
        return f"{self.brand}: Beep beep!"

class ElectricCar(Car):
    def __init__(self, brand, speed, doors, battery_kWh):
        super().__init__(brand, speed, doors)
        self.battery = battery_kWh

    def charge_status(self):
        return f"{self.brand}: Battery = {self.battery} kWh"

    def move(self):                     # override
        return f"{self.brand} silently glides at {self.speed} km/h ⚡"

tesla = ElectricCar("Tesla", 200, 4, 100)
print(tesla.move())             # overridden
print(tesla.honk())             # from Car
print(tesla.charge_status())   # own method


# ── 3. Multiple Inheritance ───────────────────────────────
print("\n=== 3. Multiple Inheritance ===")

class Flyable:
    def fly(self):
        return f"{self.__class__.__name__} is flying! ✈️"

    def altitude(self):
        return "Altitude: 10,000 m"

class Swimmable:
    def swim(self):
        return f"{self.__class__.__name__} is swimming! 🏊"

    def depth(self):
        return "Depth: 5 m"

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        Animal.__init__(self, name, "Quack")

    def describe(self):
        return f"{self.name} can fly, swim, and quack!"

donald = Duck("Donald")
print(donald.speak())
print(donald.fly())
print(donald.swim())
print(donald.describe())
print("MRO:", [c.__name__ for c in Duck.__mro__])


# ── 4. Method Overriding ──────────────────────────────────
print("\n=== 4. Method Overriding ===")

class Shape:
    def __init__(self, color="black"):
        self.color = color

    def area(self):
        return 0

    def describe(self):
        return f"{self.__class__.__name__} | Color: {self.color} | Area: {self.area():.2f}"

class Circle(Shape):
    import math
    def __init__(self, radius, color="red"):
        super().__init__(color)
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

class Triangle(Shape):
    def __init__(self, base, height, color="blue"):
        super().__init__(color)
        self.base   = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

class Square(Shape):
    def __init__(self, side, color="green"):
        super().__init__(color)
        self.side = side

    def area(self):
        return self.side ** 2

shapes = [Circle(5), Triangle(6, 4), Square(3), Shape()]
for shape in shapes:
    print(" ", shape.describe())


# ── 5. super() in depth ───────────────────────────────────
print("\n=== 5. super() with Cooperative Multiple Inheritance ===")

class A:
    def greet(self):
        print("  Hello from A")

class B(A):
    def greet(self):
        print("  Hello from B")
        super().greet()

class C(A):
    def greet(self):
        print("  Hello from C")
        super().greet()

class D(B, C):
    def greet(self):
        print("  Hello from D")
        super().greet()

d = D()
d.greet()
print("  MRO:", [c.__name__ for c in D.__mro__])


# ── 6. isinstance() and issubclass() ─────────────────────
print("\n=== 6. isinstance() & issubclass() ===")

print(f"tesla isinstance Car?      {isinstance(tesla, Car)}")
print(f"tesla isinstance Vehicle?  {isinstance(tesla, Vehicle)}")
print(f"tesla isinstance Shape?    {isinstance(tesla, Shape)}")
print(f"ElectricCar issubclass Car?     {issubclass(ElectricCar, Car)}")
print(f"ElectricCar issubclass Vehicle? {issubclass(ElectricCar, Vehicle)}")
print(f"type of tesla:             {type(tesla).__name__}")


# ── 7. Abstract Base Class ────────────────────────────────
print("\n=== 7. Abstract Base Classes (abc) ===")
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def pay(self):
        """Every payment method MUST implement this."""
        pass

    @abstractmethod
    def refund(self):
        pass

    def receipt(self):
        return f"Receipt: ₹{self.amount} via {self.__class__.__name__}"

class CreditCard(PaymentMethod):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.card = "**** **** **** " + str(card_number)[-4:]

    def pay(self):
        return f"💳 Paid ₹{self.amount} via Credit Card {self.card}"

    def refund(self):
        return f"↩️  Refunded ₹{self.amount} to Credit Card"

class UPI(PaymentMethod):
    def __init__(self, amount, upi_id):
        super().__init__(amount)
        self.upi_id = upi_id

    def pay(self):
        return f"📱 Paid ₹{self.amount} via UPI ({self.upi_id})"

    def refund(self):
        return f"↩️  Refunded ₹{self.amount} to UPI ({self.upi_id})"

payments = [CreditCard(1500, "1234567890123456"), UPI(800, "alice@upi")]
for p in payments:
    print(" ", p.pay())
    print(" ", p.receipt())
    print(" ", p.refund())
    print()
