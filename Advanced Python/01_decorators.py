# ============================================================
#  Topic 1: Decorators
#  Covers: basic, *args/**kwargs, timer, retry, memoize,
#          validate, access control, stacking, class decorators
# ============================================================

import time, functools, random

# ── 1. Basic Decorator ────────────────────────────────────
print("=== 1. Basic Decorator ===")

def my_decorator(func):
    def wrapper():
        print("  ── Before ──")
        func()
        print("  ── After ──")
    return wrapper

@my_decorator
def say_hello():
    print("  Hello World!")

say_hello()

# ── 2. Decorator preserving function metadata ─────────────
print("\n=== 2. @functools.wraps ===")

def log_calls(func):
    @functools.wraps(func)          # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        print(f"  📞 Calling '{func.__name__}' args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"  ✅ Returned: {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b

add(3, 5)
print(f"  Name: {add.__name__} | Doc: {add.__doc__}")

# ── 3. Timer decorator ────────────────────────────────────
print("\n=== 3. Timer Decorator ===")

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  ⏱️  '{func.__name__}' took {elapsed:.6f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(1_000_000)

# ── 4. Parametrized decorator ─────────────────────────────
print("\n=== 4. Parametrized Decorator (Retry) ===")

def retry(max_attempts=3, delay=0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  ⚠️  Attempt {attempt}/{max_attempts}: {e}")
                    if attempt < max_attempts: time.sleep(delay)
            raise RuntimeError(f"Failed after {max_attempts} attempts.")
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0)
def flaky():
    if random.random() < 0.7: raise ValueError("Random failure!")
    return "✅ Success!"

try:
    print(f"  {flaky()}")
except RuntimeError as e:
    print(f"  ❌ {e}")

# ── 5. Memoize decorator ──────────────────────────────────
print("\n=== 5. Memoize Decorator ===")

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

print(f"  fib(40) = {fib(40)}")

from functools import lru_cache
@lru_cache(maxsize=128)
def fib_lru(n):
    if n <= 1: return n
    return fib_lru(n-1) + fib_lru(n-2)

print(f"  fib_lru(50) = {fib_lru(50)}")

# ── 6. Role-based access control ─────────────────────────
print("\n=== 6. Access Control Decorator ===")

def requires_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                raise PermissionError(f"'{user['name']}' needs role '{role}'")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@requires_role("admin")
def delete_record(user, record_id):
    return f"Deleted record {record_id} by {user['name']}"

admin = {"name": "Alice", "role": "admin"}
guest = {"name": "Bob",   "role": "guest"}
print(f"  {delete_record(admin, 42)}")
try:
    delete_record(guest, 42)
except PermissionError as e:
    print(f"  ❌ {e}")

# ── 7. Stacking decorators ────────────────────────────────
print("\n=== 7. Stacking Decorators ===")

@timer
@log_calls
def power(base, exp):
    return base ** exp

power(2, 10)

# ── 8. Class-based decorator ─────────────────────────────
print("\n=== 8. Class-Based Decorator ===")

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"  Call #{self.count} to '{self.func.__name__}'")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hi, {name}!"

greet("Alice"); greet("Bob"); greet("Carol")
print(f"  Total calls: {greet.count}")
