# ============================================================
#  Topic 3: Stack & Queue
#  Covers: Stack (LIFO), Queue (FIFO), Deque, Priority Queue,
#          interview problems: balanced brackets, next greater
# ============================================================

from collections import deque
import heapq

# ────────────────────────────────────────────────────────────
#  STACK  (LIFO — Last In First Out)
# ────────────────────────────────────────────────────────────

class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):       self._data.append(item)
    def pop(self):
        if self.is_empty(): raise IndexError("Stack is empty")
        return self._data.pop()
    def peek(self):
        if self.is_empty(): raise IndexError("Stack is empty")
        return self._data[-1]
    def is_empty(self):         return len(self._data) == 0
    def size(self):             return len(self._data)
    def __str__(self):          return f"Stack{self._data} ← top"


# ────────────────────────────────────────────────────────────
#  QUEUE  (FIFO — First In First Out)
# ────────────────────────────────────────────────────────────

class Queue:
    def __init__(self):
        self._data = deque()    # deque for O(1) enqueue/dequeue

    def enqueue(self, item):    self._data.append(item)
    def dequeue(self):
        if self.is_empty(): raise IndexError("Queue is empty")
        return self._data.popleft()
    def front(self):
        if self.is_empty(): raise IndexError("Queue is empty")
        return self._data[0]
    def is_empty(self):         return len(self._data) == 0
    def size(self):             return len(self._data)
    def __str__(self):          return f"Queue front→{list(self._data)}←rear"


# ────────────────────────────────────────────────────────────
#  DEQUE  (Double-ended queue)
# ────────────────────────────────────────────────────────────

class Deque:
    def __init__(self):
        self._data = deque()

    def add_front(self, item):  self._data.appendleft(item)
    def add_rear(self, item):   self._data.append(item)
    def remove_front(self):     return self._data.popleft()
    def remove_rear(self):      return self._data.pop()
    def peek_front(self):       return self._data[0]
    def peek_rear(self):        return self._data[-1]
    def is_empty(self):         return len(self._data) == 0
    def size(self):             return len(self._data)
    def __str__(self):          return f"Deque{list(self._data)}"


# ────────────────────────────────────────────────────────────
#  PRIORITY QUEUE (min-heap via heapq)
# ────────────────────────────────────────────────────────────

class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        if not self._heap: raise IndexError("Priority queue is empty")
        priority, item = heapq.heappop(self._heap)
        return item, priority

    def peek(self):
        return self._heap[0][1], self._heap[0][0]

    def is_empty(self):     return len(self._heap) == 0
    def size(self):         return len(self._heap)
    def __str__(self):      return f"PQ{self._heap}"


# ────────────────────────────────────────────────────────────
#  STACK INTERVIEW PROBLEMS
# ────────────────────────────────────────────────────────────

def balanced_brackets(s):
    """Check if brackets are balanced — classic stack problem"""
    stack = Stack()
    pairs = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in "({[": stack.push(c)
        elif c in ")}]":
            if stack.is_empty() or stack.peek() != pairs[c]:
                return False
            stack.pop()
    return stack.is_empty()


def evaluate_postfix(expr):
    """Evaluate postfix expression — e.g. '3 4 + 2 *'"""
    stack = Stack()
    for token in expr.split():
        if token.lstrip('-').isdigit():
            stack.push(int(token))
        else:
            b, a = stack.pop(), stack.pop()
            if token == '+': stack.push(a + b)
            elif token == '-': stack.push(a - b)
            elif token == '*': stack.push(a * b)
            elif token == '/': stack.push(int(a / b))
    return stack.pop()


def next_greater_element(arr):
    """For each element, find the next greater element — O(n)"""
    result = [-1] * len(arr)
    stack = Stack()          # stores indices
    for i in range(len(arr)):
        while not stack.is_empty() and arr[i] > arr[stack.peek()]:
            idx = stack.pop()
            result[idx] = arr[i]
        stack.push(i)
    return result


def sort_stack(stack):
    """Sort a stack using only one extra stack — O(n²)"""
    sorted_stack = Stack()
    while not stack.is_empty():
        temp = stack.pop()
        while not sorted_stack.is_empty() and sorted_stack.peek() > temp:
            stack.push(sorted_stack.pop())
        sorted_stack.push(temp)
    return sorted_stack


def min_stack_demo():
    """Stack that supports getMin() in O(1)"""
    class MinStack:
        def __init__(self):
            self._data = []
            self._mins = []         # tracks minimums

        def push(self, val):
            self._data.append(val)
            if not self._mins or val <= self._mins[-1]:
                self._mins.append(val)

        def pop(self):
            val = self._data.pop()
            if val == self._mins[-1]:
                self._mins.pop()
            return val

        def get_min(self): return self._mins[-1]
        def top(self):     return self._data[-1]

    ms = MinStack()
    for v in [5, 3, 7, 2, 8, 1]:
        ms.push(v)
        print(f"  Pushed {v} → min = {ms.get_min()}")
    ms.pop(); ms.pop()
    print(f"  After 2 pops → min = {ms.get_min()}")


# ────────────────────────────────────────────────────────────
#  QUEUE INTERVIEW PROBLEMS
# ────────────────────────────────────────────────────────────

def queue_using_stacks():
    """Implement a queue using two stacks"""
    class QueueFromStacks:
        def __init__(self):
            self.s1 = Stack()   # for enqueue
            self.s2 = Stack()   # for dequeue

        def enqueue(self, item):
            self.s1.push(item)

        def dequeue(self):
            if self.s2.is_empty():
                while not self.s1.is_empty():
                    self.s2.push(self.s1.pop())
            if self.s2.is_empty():
                raise IndexError("Queue is empty")
            return self.s2.pop()

        def front(self):
            if self.s2.is_empty():
                while not self.s1.is_empty():
                    self.s2.push(self.s1.pop())
            return self.s2.peek()

    q = QueueFromStacks()
    for v in [1, 2, 3, 4]:
        q.enqueue(v)
        print(f"  Enqueued {v}")
    print(f"  Front: {q.front()}")
    print(f"  Dequeue: {q.dequeue()}")
    print(f"  Dequeue: {q.dequeue()}")
    print(f"  Front now: {q.front()}")


def sliding_window_max(arr, k):
    """Maximum in every window of size k — O(n)"""
    if not arr or k == 0: return []
    dq = deque()    # stores indices
    result = []
    for i in range(len(arr)):
        # Remove out-of-window elements
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller elements (useless)
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(arr[dq[0]])
    return result


def bfs_using_queue(graph, start):
    """Breadth-First Search using a queue"""
    visited = set()
    queue = Queue()
    order = []
    queue.enqueue(start)
    visited.add(start)
    while not queue.is_empty():
        node = queue.dequeue()
        order.append(node)
        for neighbor in sorted(graph.get(node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
    return order


# ────────────────────────────────────────────────────────────
#  DEMO
# ────────────────────────────────────────────────────────────

print("="*50)
print("  STACK DEMO")
print("="*50)
s = Stack()
for v in [10, 20, 30]: s.push(v)
print(f"Stack: {s}")
print(f"Peek: {s.peek()}, Pop: {s.pop()}")
print(f"After pop: {s}")

print("\n"+"="*50)
print("  QUEUE DEMO")
print("="*50)
q = Queue()
for v in ['A', 'B', 'C']: q.enqueue(v)
print(f"Queue: {q}")
print(f"Front: {q.front()}, Dequeue: {q.dequeue()}")
print(f"After dequeue: {q}")

print("\n"+"="*50)
print("  PRIORITY QUEUE DEMO")
print("="*50)
pq = PriorityQueue()
pq.push("Low priority task",   priority=3)
pq.push("High priority task",  priority=1)
pq.push("Medium priority task",priority=2)
while not pq.is_empty():
    item, pri = pq.pop()
    print(f"  [{pri}] {item}")

print("\n"+"="*50)
print("  INTERVIEW PROBLEMS")
print("="*50)

exprs = ["(())", "([{}])", "(()", "([)]"]
for e in exprs:
    print(f"\nBalanced '{e}': {balanced_brackets(e)}")

postfix = "3 4 + 2 * 7 -"
print(f"\nPostfix '{postfix}' = {evaluate_postfix(postfix)}")

arr = [4, 5, 2, 10, 8]
print(f"\nNext greater {arr}: {next_greater_element(arr)}")

st = Stack()
for v in [5, 1, 4, 2, 8]: st.push(v)
sorted_st = sort_stack(st)
print(f"\nSorted stack: ", end="")
while not sorted_st.is_empty(): print(sorted_st.pop(), end=" ")

print("\n\n── MinStack ──")
min_stack_demo()

print("\n── Queue from 2 Stacks ──")
queue_using_stacks()

arr2 = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(f"\nSliding window max {arr2}, k={k}: {sliding_window_max(arr2, k)}")

graph = {1:[2,3], 2:[4,5], 3:[5], 4:[], 5:[6], 6:[]}
print(f"\nBFS from node 1: {bfs_using_queue(graph, 1)}")
