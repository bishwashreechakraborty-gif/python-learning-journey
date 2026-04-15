# ============================================================
#  Practice: 20 Classic Interview Problems
#  LeetCode / GeeksforGeeks / CodeStudio style
#  Topics: Arrays, Strings, Linked List, Stack, Tree, DP
# ============================================================

from collections import defaultdict, deque
import heapq

print("=" * 60)
print("  20 CLASSIC INTERVIEW PROBLEMS")
print("=" * 60)

# ────────────────────────────────────────────────────────────
#  ARRAYS
# ────────────────────────────────────────────────────────────

# P1. Contains Duplicate  [Easy — LeetCode 217]
def contains_duplicate(nums):
    """Return True if any value appears at least twice."""
    return len(nums) != len(set(nums))

print("\nP01. Contains Duplicate")
print(f"  [1,2,3,1] → {contains_duplicate([1,2,3,1])}")
print(f"  [1,2,3,4] → {contains_duplicate([1,2,3,4])}")


# P2. Best Time to Buy and Sell Stock  [Easy — LeetCode 121]
def max_profit(prices):
    """Find max profit from one buy then one sell."""
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

print("\nP02. Best Time to Buy & Sell Stock")
print(f"  [7,1,5,3,6,4] → profit = {max_profit([7,1,5,3,6,4])}")
print(f"  [7,6,4,3,1]   → profit = {max_profit([7,6,4,3,1])}")


# P3. Product of Array Except Self  [Medium — LeetCode 238]
def product_except_self(nums):
    """Return array where result[i] = product of all except nums[i]. No division."""
    n = len(nums)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result

print("\nP03. Product Except Self")
print(f"  [1,2,3,4] → {product_except_self([1,2,3,4])}")


# P4. Maximum Product Subarray  [Medium — LeetCode 152]
def max_product(nums):
    max_p = min_p = result = nums[0]
    for n in nums[1:]:
        choices = (n, max_p * n, min_p * n)
        max_p = max(choices)
        min_p = min(choices)
        result = max(result, max_p)
    return result

print("\nP04. Maximum Product Subarray")
print(f"  [2,3,-2,4] → {max_product([2,3,-2,4])}")
print(f"  [-2,0,-1]  → {max_product([-2,0,-1])}")


# P5. 3Sum  [Medium — LeetCode 15]
def three_sum(nums):
    """Find all unique triplets that sum to zero."""
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]: continue   # skip duplicates
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]: left += 1
                while left < right and nums[right] == nums[right-1]: right -= 1
                left += 1; right -= 1
            elif total < 0: left += 1
            else: right -= 1
    return result

print("\nP05. 3Sum")
print(f"  [-1,0,1,2,-1,-4] → {three_sum([-1,0,1,2,-1,-4])}")


# ────────────────────────────────────────────────────────────
#  STRINGS
# ────────────────────────────────────────────────────────────

# P6. Longest Substring Without Repeating Characters  [Medium — LC 3]
def length_of_longest_substring(s):
    char_idx = {}
    max_len = start = 0
    for end, char in enumerate(s):
        if char in char_idx and char_idx[char] >= start:
            start = char_idx[char] + 1
        char_idx[char] = end
        max_len = max(max_len, end - start + 1)
    return max_len

print("\nP06. Longest Substring Without Repeating Chars")
for s in ["abcabcbb", "bbbbb", "pwwkew"]:
    print(f"  '{s}' → {length_of_longest_substring(s)}")


# P7. Group Anagrams  [Medium — LeetCode 49]
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())

print("\nP07. Group Anagrams")
print(f"  {group_anagrams(['eat','tea','tan','ate','nat','bat'])}")


# P8. Valid Palindrome  [Easy — LeetCode 125]
def is_valid_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

print("\nP08. Valid Palindrome")
print(f"  'A man, a plan, a canal: Panama' → {is_valid_palindrome('A man, a plan, a canal: Panama')}")
print(f"  'race a car' → {is_valid_palindrome('race a car')}")


# P9. Longest Palindromic Substring  [Medium — LeetCode 5]
def longest_palindrome(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1; right += 1
        return s[left+1:right]
    result = ""
    for i in range(len(s)):
        odd  = expand(i, i)
        even = expand(i, i+1)
        result = max(result, odd, even, key=len)
    return result

print("\nP09. Longest Palindromic Substring")
for s in ["babad", "cbbd", "racecar"]:
    print(f"  '{s}' → '{longest_palindrome(s)}'")


# ────────────────────────────────────────────────────────────
#  LINKED LIST (using simple nodes)
# ────────────────────────────────────────────────────────────

class Node:
    def __init__(self, val=0, nxt=None):
        self.val = val; self.next = nxt

def list_to_ll(values):
    dummy = Node()
    curr = dummy
    for v in values: curr.next = Node(v); curr = curr.next
    return dummy.next

def ll_to_list(head):
    result = []
    while head: result.append(head.val); head = head.next
    return result


# P10. Reverse a Linked List  [Easy — LeetCode 206]
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

print("\nP10. Reverse Linked List")
ll = list_to_ll([1,2,3,4,5])
print(f"  [1,2,3,4,5] → {ll_to_list(reverse_list(ll))}")


# P11. Merge Two Sorted Lists  [Easy — LeetCode 21]
def merge_two_lists(l1, l2):
    dummy = Node()
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val: curr.next = l1; l1 = l1.next
        else: curr.next = l2; l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

print("\nP11. Merge Two Sorted Lists")
l1 = list_to_ll([1,2,4]); l2 = list_to_ll([1,3,4])
print(f"  [1,2,4] + [1,3,4] → {ll_to_list(merge_two_lists(l1, l2))}")


# ────────────────────────────────────────────────────────────
#  STACK & QUEUE
# ────────────────────────────────────────────────────────────

# P12. Valid Parentheses  [Easy — LeetCode 20]
def is_valid_parens(s):
    stack = []
    pairs = {')':'(', '}':'{', ']':'['}
    for c in s:
        if c in "({[": stack.append(c)
        elif not stack or stack[-1] != pairs[c]: return False
        else: stack.pop()
    return not stack

print("\nP12. Valid Parentheses")
for s in ["()", "()[]{}", "(]", "([)]", "{[]}"]:
    print(f"  '{s}' → {is_valid_parens(s)}")


# P13. Daily Temperatures  [Medium — LeetCode 739]
def daily_temperatures(temps):
    """For each day, how many days until a warmer day?"""
    result = [0] * len(temps)
    stack = []  # indices
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    return result

print("\nP13. Daily Temperatures")
temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(f"  {temps}")
print(f"  → {daily_temperatures(temps)}")


# ────────────────────────────────────────────────────────────
#  BINARY TREE
# ────────────────────────────────────────────────────────────

class TNode:
    def __init__(self, val, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def build_tree(values):
    if not values: return None
    root = TNode(values[0])
    queue = deque([root]); i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TNode(values[i]); queue.append(node.right)
        i += 1
    return root


# P14. Maximum Depth of Binary Tree  [Easy — LeetCode 104]
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

print("\nP14. Max Depth of Binary Tree")
t = build_tree([3,9,20,None,None,15,7])
print(f"  [3,9,20,null,null,15,7] → depth {max_depth(t)}")


# P15. Path Sum  [Easy — LeetCode 112]
def has_path_sum(root, target):
    """Does any root-to-leaf path sum to target?"""
    if not root: return False
    if not root.left and not root.right: return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))

print("\nP15. Path Sum")
t2 = build_tree([5,4,8,11,None,13,4,7,2,None,None,None,1])
print(f"  Target 22 → {has_path_sum(t2, 22)}")
print(f"  Target 99 → {has_path_sum(t2, 99)}")


# P16. Symmetric Tree  [Easy — LeetCode 101]
def is_symmetric(root):
    def mirror(left, right):
        if not left and not right: return True
        if not left or not right:  return False
        return (left.val == right.val and
                mirror(left.left, right.right) and
                mirror(left.right, right.left))
    return mirror(root.left, root.right) if root else True

print("\nP16. Symmetric Tree")
sym = build_tree([1,2,2,3,4,4,3])
asym = build_tree([1,2,2,None,3,None,3])
print(f"  [1,2,2,3,4,4,3] → {is_symmetric(sym)}")
print(f"  [1,2,2,null,3,null,3] → {is_symmetric(asym)}")


# ────────────────────────────────────────────────────────────
#  DYNAMIC PROGRAMMING
# ────────────────────────────────────────────────────────────

# P17. Climbing Stairs  [Easy — LeetCode 70]
def climb_stairs(n):
    """How many ways to climb n stairs taking 1 or 2 steps at a time?"""
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n+1):
        a, b = b, a + b
    return b

print("\nP17. Climbing Stairs")
for n in range(1, 8):
    print(f"  n={n} → {climb_stairs(n)} ways")


# P18. Coin Change  [Medium — LeetCode 322]
def coin_change(coins, amount):
    """Minimum coins to make `amount`. Return -1 if impossible."""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

print("\nP18. Coin Change")
print(f"  coins=[1,5,11], amount=15 → {coin_change([1,5,11], 15)} coins")
print(f"  coins=[2], amount=3 → {coin_change([2], 3)}")


# P19. Longest Common Subsequence  [Medium — LeetCode 1143]
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]: dp[i][j] = 1 + dp[i-1][j-1]
            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

print("\nP19. Longest Common Subsequence")
pairs = [("abcde","ace"), ("abc","abc"), ("abc","def")]
for t1, t2 in pairs:
    print(f"  LCS('{t1}', '{t2}') = {lcs(t1, t2)}")


# P20. House Robber  [Easy — LeetCode 198]
def rob(nums):
    """Max money from non-adjacent houses."""
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    prev2, prev1 = 0, 0
    for n in nums:
        curr = max(prev1, prev2 + n)
        prev2, prev1 = prev1, curr
    return prev1

print("\nP20. House Robber")
print(f"  [1,2,3,1] → {rob([1,2,3,1])}")
print(f"  [2,7,9,3,1] → {rob([2,7,9,3,1])}")

print("\n" + "="*60)
print("  PROBLEM DIFFICULTY SUMMARY")
print("="*60)
print("""
  Easy   (practice daily): P1,P2,P8,P10,P11,P12,P14,P15,P16,P17,P20
  Medium (stretch goals)  : P3,P4,P5,P6,P7,P9,P13,P18,P19

  Recommended Platforms:
    • LeetCode   → https://leetcode.com
    • GFG        → https://geeksforgeeks.org
    • CodeStudio → https://codingninjas.com

  Daily Plan:
    Day 1–7  : Do 1 Easy problem/day
    Day 8–15 : Do 1 Easy + attempt 1 Medium
    Day 16+  : 1 Medium/day + revisit Mediums
""")
