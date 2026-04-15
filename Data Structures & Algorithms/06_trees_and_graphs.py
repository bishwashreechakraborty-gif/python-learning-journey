# ============================================================
#  Topic 6: Trees & Graphs (Basic)
#  Covers: Binary Tree, BST, BFS, DFS, Graph representation
# ============================================================

from collections import deque, defaultdict

# ────────────────────────────────────────────────────────────
#  BINARY TREE
# ────────────────────────────────────────────────────────────

class TreeNode:
    def __init__(self, val):
        self.val   = val
        self.left  = None
        self.right = None

    def __repr__(self): return f"TreeNode({self.val})"


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert_level_order(self, values):
        """Build tree from list level-by-level (None = no node)."""
        if not values or values[0] is None: return
        self.root = TreeNode(values[0])
        queue = deque([self.root])
        i = 1
        while queue and i < len(values):
            node = queue.popleft()
            if i < len(values) and values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
            if i < len(values) and values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1

    # ── Traversals ────────────────────────────────────────
    def inorder(self, node=None, first=True):
        """Left → Root → Right"""
        if first: node = self.root
        if not node: return []
        return self.inorder(node.left, False) + [node.val] + self.inorder(node.right, False)

    def preorder(self, node=None, first=True):
        """Root → Left → Right"""
        if first: node = self.root
        if not node: return []
        return [node.val] + self.preorder(node.left, False) + self.preorder(node.right, False)

    def postorder(self, node=None, first=True):
        """Left → Right → Root"""
        if first: node = self.root
        if not node: return []
        return self.postorder(node.left, False) + self.postorder(node.right, False) + [node.val]

    def level_order(self):
        """BFS traversal — level by level"""
        if not self.root: return []
        result, queue = [], deque([self.root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
            result.append(level)
        return result

    # ── Tree properties ───────────────────────────────────
    def height(self, node=None, first=True):
        if first: node = self.root
        if not node: return 0
        return 1 + max(self.height(node.left, False), self.height(node.right, False))

    def count_nodes(self, node=None, first=True):
        if first: node = self.root
        if not node: return 0
        return 1 + self.count_nodes(node.left,False) + self.count_nodes(node.right,False)

    def is_balanced(self, node=None, first=True):
        """Check if tree is height-balanced."""
        if first: node = self.root
        if not node: return True

        def check(n):
            if not n: return 0
            left_h = check(n.left)
            if left_h == -1: return -1
            right_h = check(n.right)
            if right_h == -1: return -1
            if abs(left_h - right_h) > 1: return -1
            return 1 + max(left_h, right_h)

        return check(node) != -1

    def max_depth(self): return self.height()

    def sum_all(self, node=None, first=True):
        if first: node = self.root
        if not node: return 0
        return node.val + self.sum_all(node.left,False) + self.sum_all(node.right,False)

    def print_tree(self):
        """Simple visual representation."""
        levels = self.level_order()
        for i, level in enumerate(levels):
            indent = "  " * (len(levels) - i)
            print(indent + "  ".join(str(v) for v in level))


# ────────────────────────────────────────────────────────────
#  BINARY SEARCH TREE
# ────────────────────────────────────────────────────────────

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        def _insert(node, val):
            if not node: return TreeNode(val)
            if val < node.val:  node.left  = _insert(node.left, val)
            elif val > node.val: node.right = _insert(node.right, val)
            return node
        self.root = _insert(self.root, val)

    def search(self, val):
        def _search(node, val):
            if not node: return False
            if node.val == val: return True
            if val < node.val: return _search(node.left, val)
            return _search(node.right, val)
        return _search(self.root, val)

    def delete(self, val):
        def _delete(node, val):
            if not node: return node
            if val < node.val:  node.left  = _delete(node.left, val)
            elif val > node.val: node.right = _delete(node.right, val)
            else:
                if not node.left:  return node.right
                if not node.right: return node.left
                # Find inorder successor (min of right subtree)
                curr = node.right
                while curr.left: curr = curr.left
                node.val = curr.val
                node.right = _delete(node.right, curr.val)
            return node
        self.root = _delete(self.root, val)

    def inorder(self, node=None, first=True):
        if first: node = self.root
        if not node: return []
        return self.inorder(node.left,False) + [node.val] + self.inorder(node.right,False)

    def min_val(self):
        node = self.root
        while node.left: node = node.left
        return node.val

    def max_val(self):
        node = self.root
        while node.right: node = node.right
        return node.val

    def is_valid_bst(self):
        """Validate that BST property holds everywhere."""
        def validate(node, mn=float('-inf'), mx=float('inf')):
            if not node: return True
            if node.val <= mn or node.val >= mx: return False
            return (validate(node.left, mn, node.val) and
                    validate(node.right, node.val, mx))
        return validate(self.root)


# ────────────────────────────────────────────────────────────
#  GRAPH
# ────────────────────────────────────────────────────────────

class Graph:
    def __init__(self, directed=False):
        self.adj = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def neighbors(self, v): return [n for n,_ in self.adj[v]]

    # ── BFS — O(V + E) ────────────────────────────────────
    def bfs(self, start):
        visited, order = {start}, [start]
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in sorted(self.neighbors(node)):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    order.append(neighbor)
        return order

    # ── DFS — O(V + E) ────────────────────────────────────
    def dfs(self, start, visited=None):
        if visited is None: visited = set()
        visited.add(start)
        order = [start]
        for neighbor in sorted(self.neighbors(start)):
            if neighbor not in visited:
                order.extend(self.dfs(neighbor, visited))
        return order

    def dfs_iterative(self, start):
        visited, order = set(), []
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor in sorted(self.neighbors(node), reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return order

    # ── Cycle detection ───────────────────────────────────
    def has_cycle_undirected(self):
        visited = set()
        def dfs(v, parent):
            visited.add(v)
            for neighbor in self.neighbors(v):
                if neighbor not in visited:
                    if dfs(neighbor, v): return True
                elif neighbor != parent:
                    return True
            return False
        for v in self.adj:
            if v not in visited:
                if dfs(v, -1): return True
        return False

    # ── Shortest path (unweighted — BFS) ──────────────────
    def shortest_path(self, start, end):
        if start == end: return [start], 0
        visited = {start}
        queue = deque([(start, [start])])
        while queue:
            node, path = queue.popleft()
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    if neighbor == end:
                        return new_path, len(new_path)-1
                    visited.add(neighbor)
                    queue.append((neighbor, new_path))
        return None, -1

    # ── Connected components ──────────────────────────────
    def connected_components(self):
        visited, components = set(), []
        for v in self.adj:
            if v not in visited:
                component = self.dfs(v, visited)
                components.append(component)
        return components

    def __str__(self):
        lines = [f"Graph ({'directed' if self.directed else 'undirected'}):"]
        for v in sorted(self.adj.keys()):
            neighbors = [f"{n}(w={w})" if w!=1 else str(n) for n,w in self.adj[v]]
            lines.append(f"  {v} → {neighbors}")
        return "\n".join(lines)


# ────────────────────────────────────────────────────────────
#  DEMO
# ────────────────────────────────────────────────────────────

print("=" * 55)
print("  BINARY TREE DEMO")
print("=" * 55)

bt = BinaryTree()
bt.insert_level_order([1, 2, 3, 4, 5, 6, 7])
print(f"\nTree structure:")
bt.print_tree()
print(f"\nInorder   : {bt.inorder()}")
print(f"Preorder  : {bt.preorder()}")
print(f"Postorder : {bt.postorder()}")
print(f"Level-order: {bt.level_order()}")
print(f"\nHeight    : {bt.height()}")
print(f"Nodes     : {bt.count_nodes()}")
print(f"Sum       : {bt.sum_all()}")
print(f"Balanced  : {bt.is_balanced()}")

print("\n\n" + "=" * 55)
print("  BINARY SEARCH TREE DEMO")
print("=" * 55)

bst = BST()
for val in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(val)

print(f"\nInorder (sorted): {bst.inorder()}")
print(f"Min: {bst.min_val()}, Max: {bst.max_val()}")
print(f"Search 40: {bst.search(40)}")
print(f"Search 99: {bst.search(99)}")
print(f"Valid BST: {bst.is_valid_bst()}")

bst.delete(30)
print(f"After deleting 30: {bst.inorder()}")

print("\n\n" + "=" * 55)
print("  GRAPH DEMO")
print("=" * 55)

g = Graph(directed=False)
edges = [(1,2), (1,3), (2,4), (2,5), (3,6), (4,7), (5,7)]
for u, v in edges:
    g.add_edge(u, v)

print(f"\n{g}")
print(f"\nBFS from 1: {g.bfs(1)}")
print(f"DFS from 1: {g.dfs(1)}")
print(f"Has cycle : {g.has_cycle_undirected()}")

path, dist = g.shortest_path(1, 7)
print(f"Shortest path 1→7: {path} (distance={dist})")

g2 = Graph()
g2.add_edge(1, 2); g2.add_edge(3, 4); g2.add_edge(5, 6)
g2.add_vertex(7)
print(f"\nConnected components of g2: {g2.connected_components()}")

print("\n\n" + "=" * 55)
print("  KEY CONCEPTS SUMMARY")
print("=" * 55)
print("""
  Tree Traversals:
    Inorder   (L-Root-R) → gives sorted order for BST
    Preorder  (Root-L-R) → used to copy/serialize a tree
    Postorder (L-R-Root) → used to delete a tree
    Level-order          → BFS on tree

  BST Property:
    left.val < node.val < right.val

  Graph Algorithms:
    BFS → shortest path (unweighted), level traversal
    DFS → cycle detection, connected components, topological sort

  Complexities:
    BFS/DFS          : O(V + E)
    BST Search/Insert: O(log n) avg, O(n) worst
    BST Balanced     : O(log n) guaranteed (AVL/Red-Black)
""")
