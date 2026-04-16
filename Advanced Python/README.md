# 🔬 Advanced Python

> **Goal:** Write professional, efficient, and modern Python code

---

## 📁 Folder Structure

```
advanced_python/
└── topics/
    ├── 01_decorators.py                    ← Wrappers, timer, retry, memoize, access control
    ├── 02_generators.py                    ← yield, lazy evaluation, pipelines, send()
    ├── 03_lambda_functions.py              ← map, filter, reduce, sorted, HOF
    ├── 04_multithreading_multiprocessing.py← Threads, Locks, Queues, Processes, GIL
    ├── 05_virtual_environments.py          ← venv, pip, requirements.txt guide
    └── 06_apis_requests.py                 ← GET/POST/PUT/DELETE, REST, error handling
```

---

## 📚 Topics

| File | Key Concepts |
|------|-------------|
| `01_decorators.py` | `@functools.wraps`, timer, retry, memoize `@lru_cache`, role auth, stacking, class decorators |
| `02_generators.py` | `yield`, generator expressions, `yield from`, `send()`, infinite sequences, memory savings |
| `03_lambda_functions.py` | `lambda`, `map()`, `filter()`, `reduce()`, `sorted()` with key, function composition |
| `04_multithreading_multiprocessing.py` | `threading.Thread`, `Lock`, `Queue`, `ThreadPoolExecutor`, `multiprocessing`, GIL |
| `05_virtual_environments.py` | `python -m venv`, `pip install`, `requirements.txt`, `.gitignore` |
| `06_apis_requests.py` | `requests` GET/POST/PUT/PATCH/DELETE, headers, auth, error handling, sessions, real APIs |

---

## 🚀 Quick Start

```bash
# Run any topic file
python topics/01_decorators.py

# For APIs topic, install requests first:
pip install requests
python topics/06_apis_requests.py
```

---

## 💡 Key Concepts Summary

### Decorators
```python
import functools
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time; start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.3f}s")
        return result
    return wrapper

@timer
def my_func(): pass
```

### Generators
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(10)])
```

### Lambda + map/filter
```python
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
evens   = list(filter(lambda x: x%2==0, numbers))
```

### Threading
```python
import threading
t = threading.Thread(target=my_func, args=(arg1,))
t.start(); t.join()
```

### Requests (API)
```python
import requests
res = requests.get("https://api.example.com/data")
data = res.json()
```

---

**Python 3.7+ | `pip install requests` for Topic 6**

---

### Developed by Bishwashree Chakraborty