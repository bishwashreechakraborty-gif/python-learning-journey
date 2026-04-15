# ============================================================
#  Topic 4: Searching & Sorting
#  Covers: Linear/Binary Search, Bubble/Selection/Insertion/
#          Merge/Quick Sort with time complexity notes
# ============================================================

import time

# ────────────────────────────────────────────────────────────
#  SEARCHING ALGORITHMS
# ────────────────────────────────────────────────────────────

# 1. Linear Search — O(n)
def linear_search(arr, target):
    """Check each element one by one."""
    for i, val in enumerate(arr):
        if val == target:
            return i    # found
    return -1           # not found


# 2. Binary Search (iterative) — O(log n)  ← REQUIRES SORTED ARRAY
def binary_search(arr, target):
    """Divide and conquer on a sorted array."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:   return mid
        elif arr[mid] < target:  left  = mid + 1
        else:                    right = mid - 1
    return -1


# 3. Binary Search (recursive)
def binary_search_recursive(arr, target, left=0, right=None):
    if right is None: right = len(arr) - 1
    if left > right: return -1
    mid = (left + right) // 2
    if arr[mid] == target:   return mid
    elif arr[mid] < target:  return binary_search_recursive(arr, target, mid+1, right)
    else:                    return binary_search_recursive(arr, target, left, mid-1)


# 4. Find first and last occurrence in sorted array
def first_last_occurrence(arr, target):
    def find_first(arr, t):
        lo, hi, result = 0, len(arr)-1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == t: result = mid; hi = mid - 1
            elif arr[mid] < t: lo = mid + 1
            else: hi = mid - 1
        return result

    def find_last(arr, t):
        lo, hi, result = 0, len(arr)-1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == t: result = mid; lo = mid + 1
            elif arr[mid] < t: lo = mid + 1
            else: hi = mid - 1
        return result

    return find_first(arr, target), find_last(arr, target)


# ────────────────────────────────────────────────────────────
#  SORTING ALGORITHMS
# ────────────────────────────────────────────────────────────

# 1. Bubble Sort — O(n²) | Stable
def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped: break   # already sorted
    return arr


# 2. Selection Sort — O(n²) | Not stable
def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# 3. Insertion Sort — O(n²) avg, O(n) best | Stable
def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr


# 4. Merge Sort — O(n log n) | Stable
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]: result.append(left[i]);  i += 1
        else:                   result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


# 5. Quick Sort — O(n log n) avg, O(n²) worst | Not stable
def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# 6. Counting Sort — O(n + k) | Stable | Only integers
def counting_sort(arr, max_val=None):
    if not arr: return arr
    if max_val is None: max_val = max(arr)
    count = [0] * (max_val + 1)
    for x in arr: count[x] += 1
    result = []
    for i, c in enumerate(count):
        result.extend([i] * c)
    return result


# 7. Tim Sort (Python's built-in algorithm — best in practice)
def tim_sort(arr):
    return sorted(arr)     # Python uses Timsort internally


# ────────────────────────────────────────────────────────────
#  HELPER — benchmark
# ────────────────────────────────────────────────────────────

def benchmark(func, arr, label):
    start = time.perf_counter()
    result = func(arr.copy())
    elapsed = time.perf_counter() - start
    print(f"  {label:<22} → {elapsed*1000:.3f} ms | {result[:5]}...")


# ────────────────────────────────────────────────────────────
#  DEMO
# ────────────────────────────────────────────────────────────

print("="*55)
print("  SEARCHING ALGORITHMS")
print("="*55)

unsorted = [64, 25, 12, 22, 11, 90, 45, 33]
sorted_arr = sorted(unsorted)

print(f"\nUnsorted : {unsorted}")
print(f"Sorted   : {sorted_arr}")

target = 22
print(f"\n── Searching for {target} ──")
print(f"  Linear Search (unsorted): index {linear_search(unsorted, target)}")
print(f"  Binary Search (sorted)  : index {binary_search(sorted_arr, target)}")
print(f"  Binary (recursive)      : index {binary_search_recursive(sorted_arr, target)}")

arr2 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5]
t = 3
first, last = first_last_occurrence(arr2, t)
print(f"\nFirst/Last occurrence of {t} in {arr2}:")
print(f"  First: index {first}, Last: index {last}, Count: {last-first+1}")

print("\n\n" + "="*55)
print("  SORTING ALGORITHMS")
print("="*55)

test_arr = [64, 34, 25, 12, 22, 11, 90, 45, 55, 78, 3, 99]
print(f"\nOriginal : {test_arr}")

algorithms = [
    (bubble_sort,    "Bubble Sort    O(n²)"),
    (selection_sort, "Selection Sort O(n²)"),
    (insertion_sort, "Insertion Sort O(n²)"),
    (merge_sort,     "Merge Sort     O(nlogn)"),
    (quick_sort,     "Quick Sort     O(nlogn)"),
    (tim_sort,       "Tim Sort (Python built-in)"),
]

print(f"\nResults:")
for fn, label in algorithms:
    result = fn(test_arr)
    print(f"  {label:<32}: {result}")

print("\n── Benchmarking on 5000 elements ──")
import random
big_arr = [random.randint(0, 10000) for _ in range(5000)]
for fn, label in algorithms:
    benchmark(fn, big_arr, label)

print("\n\n" + "="*55)
print("  TIME COMPLEXITY SUMMARY")
print("="*55)
print(f"  {'Algorithm':<20} {'Best':>8} {'Avg':>10} {'Worst':>10}  Stable")
print(f"  {'─'*55}")
complexities = [
    ("Bubble Sort",    "O(n)",    "O(n²)",    "O(n²)",    "Yes"),
    ("Selection Sort", "O(n²)",   "O(n²)",    "O(n²)",    "No"),
    ("Insertion Sort", "O(n)",    "O(n²)",    "O(n²)",    "Yes"),
    ("Merge Sort",     "O(nlogn)","O(nlogn)", "O(nlogn)", "Yes"),
    ("Quick Sort",     "O(nlogn)","O(nlogn)", "O(n²)",    "No"),
    ("Counting Sort",  "O(n+k)",  "O(n+k)",   "O(n+k)",   "Yes"),
    ("Tim Sort",       "O(n)",    "O(nlogn)", "O(nlogn)", "Yes"),
]
for name, best, avg, worst, stable in complexities:
    print(f"  {name:<20} {best:>8} {avg:>10} {worst:>10}  {stable}")
