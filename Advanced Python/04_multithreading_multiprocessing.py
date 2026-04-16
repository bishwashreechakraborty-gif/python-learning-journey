# ============================================================
#  Topic 4: Multithreading & Multiprocessing
#  Covers: threading, Thread, Lock, ThreadPoolExecutor,
#          multiprocessing, ProcessPoolExecutor, GIL concept
# ============================================================

import threading
import multiprocessing
import time
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ────────────────────────────────────────────────────────────
#  PART A: THREADING
# ────────────────────────────────────────────────────────────

print("=" * 55)
print("  THREADING (I/O-bound tasks)")
print("=" * 55)

# ── 1. Basic Thread ───────────────────────────────────────
print("\n=== 1. Basic Thread ===")

def print_numbers(name, count, delay=0.1):
    for i in range(1, count + 1):
        time.sleep(delay)
        print(f"  [{name}] {i}")

# Sequential (one after another)
print("  Sequential:")
start = time.time()
print_numbers("A", 3, 0.1)
print_numbers("B", 3, 0.1)
print(f"  Time: {time.time()-start:.2f}s")

# Threaded (concurrent)
print("\n  Threaded:")
start = time.time()
t1 = threading.Thread(target=print_numbers, args=("A", 3, 0.1))
t2 = threading.Thread(target=print_numbers, args=("B", 3, 0.1))
t1.start(); t2.start()
t1.join();  t2.join()   # wait for both to finish
print(f"  Time: {time.time()-start:.2f}s")


# ── 2. Thread with daemon and name ───────────────────────
print("\n=== 2. Thread Attributes ===")

def background_task():
    for i in range(5):
        time.sleep(0.2)
        print(f"  [background] tick {i+1}")

t = threading.Thread(target=background_task, name="BackgroundThread", daemon=True)
print(f"  Thread name: {t.name}")
print(f"  Is daemon: {t.daemon}")
t.start()
time.sleep(0.5)
print(f"  Is alive: {t.is_alive()}")
t.join()


# ── 3. Thread-safe with Lock ──────────────────────────────
print("\n=== 3. Thread Safety with Lock ===")

# PROBLEM: race condition without lock
counter_unsafe = 0

def increment_unsafe():
    global counter_unsafe
    for _ in range(1000):
        counter_unsafe += 1   # NOT thread-safe!

threads = [threading.Thread(target=increment_unsafe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"  Unsafe counter (expected 5000): {counter_unsafe}")

# SOLUTION: use a Lock
counter_safe = 0
lock = threading.Lock()

def increment_safe():
    global counter_safe
    for _ in range(1000):
        with lock:
            counter_safe += 1

threads = [threading.Thread(target=increment_safe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"  Safe counter   (expected 5000): {counter_safe}")


# ── 4. Sharing data between threads ──────────────────────
print("\n=== 4. Thread Communication with Queue ===")

import queue

task_queue   = queue.Queue()
result_queue = queue.Queue()

def worker(worker_id):
    while True:
        task = task_queue.get()
        if task is None: break     # poison pill to stop worker
        result = task ** 2
        result_queue.put((worker_id, task, result))
        task_queue.task_done()

workers = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for w in workers: w.start()

for num in [1, 2, 3, 4, 5, 6]:
    task_queue.put(num)

task_queue.join()      # wait for all tasks

for _ in workers: task_queue.put(None)   # stop workers
for w in workers: w.join()

results = []
while not result_queue.empty():
    results.append(result_queue.get())

results.sort()
for worker_id, task, result in results:
    print(f"  Worker-{worker_id}: {task}² = {result}")


# ── 5. ThreadPoolExecutor ─────────────────────────────────
print("\n=== 5. ThreadPoolExecutor ===")

def fetch_url(url):
    """Simulate fetching a URL (I/O bound)."""
    time.sleep(random.uniform(0.1, 0.5))
    return f"✅ Fetched: {url} ({random.randint(100,500)}ms)"

urls = [
    "https://api.example.com/users",
    "https://api.example.com/posts",
    "https://api.example.com/comments",
    "https://api.example.com/photos",
    "https://api.example.com/todos",
]

start = time.time()
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    from concurrent.futures import as_completed
    for future in as_completed(futures):
        print(f"  {future.result()}")
print(f"  All done in {time.time()-start:.2f}s")


# ────────────────────────────────────────────────────────────
#  PART B: MULTIPROCESSING
# ────────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("  MULTIPROCESSING (CPU-bound tasks)")
print("=" * 55)

# ── 6. Basic Process ──────────────────────────────────────
print("\n=== 6. Basic Process ===")

def cpu_task(name, n):
    """CPU-bound: compute sum of squares."""
    result = sum(i**2 for i in range(n))
    print(f"  [{name}] sum of squares 0..{n}: {result:,}")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=cpu_task, args=("P1", 100000))
    p2 = multiprocessing.Process(target=cpu_task, args=("P2", 200000))
    p1.start(); p2.start()
    p1.join();  p2.join()


# ── 7. ProcessPoolExecutor ────────────────────────────────
print("\n=== 7. ProcessPoolExecutor ===")

def is_prime(n):
    """CPU-bound: check if n is prime."""
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

numbers = [2, 3, 17, 100, 997, 1000, 7919, 8000]

if __name__ == "__main__":
    start = time.time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(is_prime, numbers))
    print(f"  Primes check in {time.time()-start:.3f}s:")
    for num, prime in zip(numbers, results):
        print(f"    {num}: {'prime ✅' if prime else 'not prime ❌'}")


# ── 8. Shared Memory ─────────────────────────────────────
print("\n=== 8. Shared Memory between Processes ===")

def add_to_list(shared_list, lock, value):
    with lock:
        shared_list.append(value)

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_list = manager.list()
    lock = manager.Lock()

    processes = [
        multiprocessing.Process(target=add_to_list, args=(shared_list, lock, i))
        for i in range(10)
    ]
    for p in processes: p.start()
    for p in processes: p.join()
    print(f"  Shared list: {sorted(shared_list)}")


# ── 9. GIL Explained ─────────────────────────────────────
print("\n=== 9. GIL (Global Interpreter Lock) ===")
print("""
  Python has a GIL — only ONE thread runs Python bytecode
  at a time, even on multi-core CPUs.

  Threading is good for:  I/O-bound tasks
  → file reading, network requests, database queries
  → threads "wait" for I/O, giving others a chance

  Multiprocessing is good for:  CPU-bound tasks
  → heavy calculations, image processing, ML training
  → each process has its own GIL → true parallelism

  Rule of thumb:
  ┌─────────────────────────────────────────────────┐
  │  Task type   │  Use                             │
  ├─────────────────────────────────────────────────┤
  │  I/O-bound   │  threading / asyncio             │
  │  CPU-bound   │  multiprocessing                 │
  └─────────────────────────────────────────────────┘
""")


# ── 10. threading.Event — signaling ──────────────────────
print("\n=== 10. Event-based Thread Signaling ===")

event = threading.Event()

def wait_for_signal(name):
    print(f"  [{name}] Waiting for signal...")
    event.wait()          # blocks until event.set()
    print(f"  [{name}] Signal received! Running.")

def signal_sender():
    time.sleep(0.3)
    print("  [sender] Sending signal!")
    event.set()

threads = [threading.Thread(target=wait_for_signal, args=(f"T{i}",)) for i in range(3)]
sender  = threading.Thread(target=signal_sender)

for t in threads: t.start()
sender.start()
for t in threads: t.join()
sender.join()
