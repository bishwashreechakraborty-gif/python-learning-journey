# ============================================================
#  Topic 2: Linked List
#  Covers: Singly LL, Doubly LL, common interview problems
# ============================================================

# ────────────────────────────────────────────────────────────
#  NODE
# ────────────────────────────────────────────────────────────

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


# ────────────────────────────────────────────────────────────
#  SINGLY LINKED LIST
# ────────────────────────────────────────────────────────────

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    # ── Insertion ─────────────────────────────────────────
    def append(self, data):
        """Add to end — O(n)"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.size += 1

    def prepend(self, data):
        """Add to front — O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at(self, index, data):
        """Insert at specific index — O(n)"""
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")
        if index == 0:
            self.prepend(data); return
        new_node = Node(data)
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1

    # ── Deletion ──────────────────────────────────────────
    def delete_value(self, data):
        """Delete first occurrence of value — O(n)"""
        if not self.head: return False
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1; return True
        curr = self.head
        while curr.next:
            if curr.next.data == data:
                curr.next = curr.next.next
                self.size -= 1; return True
            curr = curr.next
        return False

    def delete_at(self, index):
        """Delete at index — O(n)"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        if index == 0:
            self.head = self.head.next
            self.size -= 1; return
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        curr.next = curr.next.next
        self.size -= 1

    # ── Search ────────────────────────────────────────────
    def search(self, data):
        """Return index of first match or -1"""
        curr, idx = self.head, 0
        while curr:
            if curr.data == data: return idx
            curr = curr.next; idx += 1
        return -1

    def get(self, index):
        """Get value at index — O(n)"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.data

    # ── Utilities ─────────────────────────────────────────
    def to_list(self):
        result, curr = [], self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def reverse(self):
        """Reverse in-place — O(n)"""
        prev, curr = None, self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def __len__(self):  return self.size
    def __str__(self):
        return " → ".join(str(x) for x in self.to_list()) + " → NULL"
    def __repr__(self): return f"LinkedList({self.to_list()})"


# ────────────────────────────────────────────────────────────
#  DOUBLY LINKED LIST
# ────────────────────────────────────────────────────────────

class DNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        node = DNode(data)
        if not self.tail:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def prepend(self, data):
        node = DNode(data)
        if not self.head:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def delete(self, data):
        curr = self.head
        while curr:
            if curr.data == data:
                if curr.prev: curr.prev.next = curr.next
                else: self.head = curr.next
                if curr.next: curr.next.prev = curr.prev
                else: self.tail = curr.prev
                self.size -= 1
                return True
            curr = curr.next
        return False

    def forward(self):
        result, curr = [], self.head
        while curr: result.append(curr.data); curr = curr.next
        return result

    def backward(self):
        result, curr = [], self.tail
        while curr: result.append(curr.data); curr = curr.prev
        return result

    def __str__(self):
        return "NULL ⇌ " + " ⇌ ".join(str(x) for x in self.forward()) + " ⇌ NULL"


# ────────────────────────────────────────────────────────────
#  INTERVIEW PROBLEMS
# ────────────────────────────────────────────────────────────

def find_middle(head):
    """Find middle node using slow/fast pointers — O(n)"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def has_cycle(head):
    """Detect cycle using Floyd's algorithm — O(n)"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast: return True
    return False

def nth_from_end(head, n):
    """Find nth node from end — O(n) single pass"""
    fast = slow = head
    for _ in range(n):
        if not fast: return None
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    return slow

def merge_sorted_lists(l1, l2):
    """Merge two sorted linked lists — O(n+m)"""
    dummy = Node(0)
    curr = dummy
    while l1 and l2:
        if l1.data <= l2.data: curr.next = l1; l1 = l1.next
        else: curr.next = l2; l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

def is_palindrome_ll(head):
    """Check if linked list is a palindrome — O(n)"""
    vals = []
    curr = head
    while curr: vals.append(curr.data); curr = curr.next
    return vals == vals[::-1]

def remove_duplicates(head):
    """Remove duplicates from unsorted LL — O(n)"""
    if not head: return head
    seen = {head.data}
    curr = head
    while curr.next:
        if curr.next.data in seen:
            curr.next = curr.next.next
        else:
            seen.add(curr.next.data)
            curr = curr.next
    return head


# ────────────────────────────────────────────────────────────
#  DEMO
# ────────────────────────────────────────────────────────────

print("=" * 50)
print("  SINGLY LINKED LIST DEMO")
print("=" * 50)

ll = LinkedList()
for v in [10, 20, 30, 40, 50]:
    ll.append(v)
print(f"Initial   : {ll}")
ll.prepend(5)
print(f"Prepend 5 : {ll}")
ll.insert_at(3, 25)
print(f"Insert 25 at idx 3: {ll}")
ll.delete_value(25)
print(f"Delete 25 : {ll}")
ll.delete_at(0)
print(f"Delete idx 0: {ll}")
print(f"Search 40 : index {ll.search(40)}")
print(f"Length    : {len(ll)}")
ll.reverse()
print(f"Reversed  : {ll}")

print("\n" + "=" * 50)
print("  DOUBLY LINKED LIST DEMO")
print("=" * 50)

dll = DoublyLinkedList()
for v in [1, 2, 3, 4, 5]:
    dll.append(v)
print(f"DLL       : {dll}")
print(f"Forward   : {dll.forward()}")
print(f"Backward  : {dll.backward()}")

print("\n" + "=" * 50)
print("  INTERVIEW PROBLEMS DEMO")
print("=" * 50)

# Build test list: 1→2→3→4→5
ll2 = LinkedList()
for v in [1, 2, 3, 4, 5]:
    ll2.append(v)

mid = find_middle(ll2.head)
print(f"\nMiddle of {ll2}: {mid.data}")

nth = nth_from_end(ll2.head, 2)
print(f"2nd from end of {ll2}: {nth.data}")

print(f"Has cycle (no cycle): {has_cycle(ll2.head)}")

# Palindrome
ll3 = LinkedList()
for v in [1, 2, 3, 2, 1]:
    ll3.append(v)
print(f"\nPalindrome {ll3}: {is_palindrome_ll(ll3.head)}")

ll4 = LinkedList()
for v in [1, 2, 3, 4, 5]:
    ll4.append(v)
print(f"Palindrome {ll4}: {is_palindrome_ll(ll4.head)}")

# Merge sorted
ll5 = LinkedList(); ll6 = LinkedList()
for v in [1, 3, 5]: ll5.append(v)
for v in [2, 4, 6]: ll6.append(v)
merged_head = merge_sorted_lists(ll5.head, ll6.head)
merged_vals = []
curr = merged_head
while curr: merged_vals.append(curr.data); curr = curr.next
print(f"\nMerge sorted {ll5.to_list()} + {ll6.to_list()}: {merged_vals}")

# Remove duplicates
ll7 = LinkedList()
for v in [1, 3, 1, 2, 3, 4, 2]:
    ll7.append(v)
print(f"\nBefore remove dupes: {ll7}")
remove_duplicates(ll7.head)
print(f"After remove dupes : {ll7}")
