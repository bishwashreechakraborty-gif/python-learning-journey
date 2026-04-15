# ============================================================
#  Topic 4: Polymorphism
#  Covers: method overriding, duck typing, operator overloading,
#          __dunder__ methods, runtime polymorphism
# ============================================================

# ── 1. Runtime Polymorphism (method overriding) ───────────
print("=== 1. Runtime Polymorphism ===")

class Notification:
    def send(self, message):
        raise NotImplementedError("Subclass must implement send()")

    def __str__(self):
        return self.__class__.__name__

class EmailNotification(Notification):
    def __init__(self, recipient):
        self.recipient = recipient

    def send(self, message):
        return f"📧 Email to {self.recipient}: '{message}'"

class SMSNotification(Notification):
    def __init__(self, phone):
        self.phone = phone

    def send(self, message):
        return f"📱 SMS to {self.phone}: '{message}'"

class PushNotification(Notification):
    def __init__(self, device_id):
        self.device = device_id

    def send(self, message):
        return f"🔔 Push to device {self.device}: '{message}'"

# Polymorphism: same method name, different behavior
notifications = [
    EmailNotification("alice@email.com"),
    SMSNotification("+91 9876543210"),
    PushNotification("device-abc-123"),
]
for notif in notifications:
    print(" ", notif.send("Your OTP is 4729"))


# ── 2. Duck Typing ────────────────────────────────────────
print("\n=== 2. Duck Typing ===")
# "If it walks like a duck and quacks like a duck, it's a duck."
# Python doesn't care about the type — only if the method exists.

class Robot:
    def speak(self):
        return "🤖 Beep boop! I am a robot."

class Parrot:
    def speak(self):
        return "🦜 Pretty Polly wants a cracker!"

class Baby:
    def speak(self):
        return "👶 Goo goo ga ga!"

class Alien:
    def speak(self):
        return "👽 Xzzt blorp grzzzt!"

def make_speak(entity):
    """Works on ANY object that has a .speak() method."""
    print(" ", entity.speak())

speakers = [Robot(), Parrot(), Baby(), Alien()]
for s in speakers:
    make_speak(s)     # works for all — no inheritance required


# ── 3. Operator Overloading ───────────────────────────────
print("\n=== 3. Operator Overloading ===")

class Vector:
    """2D Vector with full operator support."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):       # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):       # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):      # v * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):     # 3 * v
        return self.__mul__(scalar)

    def __eq__(self, other):        # v1 == v2
        return self.x == other.x and self.y == other.y

    def __abs__(self):              # abs(v) — magnitude
        import math
        return math.sqrt(self.x**2 + self.y**2)

    def __neg__(self):              # -v
        return Vector(-self.x, -self.y)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def dot(self, other):
        return self.x * other.x + self.y * other.y

v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 3  = {v1 * 3}")
print(f"2 * v2  = {2 * v2}")
print(f"|v1|    = {abs(v1):.2f}")
print(f"-v1     = {-v1}")
print(f"v1 dot v2 = {v1.dot(v2)}")
print(f"v1 == v1? {v1 == v1}")


# ── 4. Full dunder method showcase ───────────────────────
print("\n=== 4. Dunder Methods on a Stack ===")

class Stack:
    """Stack with rich dunder methods."""
    def __init__(self, *items):
        self._data = list(items)

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if not self._data:
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):
        return self._data[-1] if self._data else None

    # ── dunder methods ──────────────────────────────────
    def __len__(self):          return len(self._data)
    def __bool__(self):         return bool(self._data)
    def __contains__(self, x):  return x in self._data
    def __iter__(self):         return iter(reversed(self._data))
    def __getitem__(self, i):   return self._data[i]

    def __str__(self):
        return "Stack[" + " → ".join(str(x) for x in reversed(self._data)) + "]"

    def __repr__(self):
        return f"Stack({self._data})"

    def __add__(self, other):   # merge two stacks
        merged = Stack()
        merged._data = self._data + other._data
        return merged

s = Stack(1, 2, 3)
s.push(4)
print(s)
print(f"len: {len(s)}, peek: {s.peek()}, bool: {bool(s)}")
print(f"3 in stack? {3 in s}")
print(f"Iterating: {list(s)}")
print(f"s[0]: {s[0]}")
s2 = Stack(5, 6)
print(f"s + s2: {s + s2}")
print(f"Popped: {s.pop()}")


# ── 5. Polymorphism in a real scenario ───────────────────
print("\n=== 5. Polymorphism: File Exporters ===")

class Exporter:
    def export(self, data, filename):
        raise NotImplementedError

class CSVExporter(Exporter):
    def export(self, data, filename):
        rows = "\n".join(",".join(str(v) for v in row) for row in data)
        print(f"  📄 CSV → {filename}.csv:\n{rows}\n")

class JSONExporter(Exporter):
    import json
    def export(self, data, filename):
        import json
        headers = data[0]
        records = [dict(zip(headers, row)) for row in data[1:]]
        print(f"  📦 JSON → {filename}.json:")
        print(json.dumps(records, indent=2))

class MarkdownExporter(Exporter):
    def export(self, data, filename):
        header = "| " + " | ".join(str(h) for h in data[0]) + " |"
        sep    = "| " + " | ".join("---" for _ in data[0]) + " |"
        rows   = "\n".join("| " + " | ".join(str(v) for v in row) + " |"
                           for row in data[1:])
        print(f"  📝 Markdown → {filename}.md:")
        print(f"{header}\n{sep}\n{rows}\n")

data = [
    ["Name",  "Age", "Grade"],
    ["Alice",  20,   "A"],
    ["Bob",    22,   "B"],
]

for exporter in [CSVExporter(), JSONExporter(), MarkdownExporter()]:
    exporter.export(data, "students")
