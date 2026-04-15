# ============================================================
#  Topic 1: Arrays & Strings
#  Classic problems commonly asked in placements & internships
# ============================================================

# ────────────────────────────────────────────────────────────
#  ARRAYS
# ────────────────────────────────────────────────────────────

print("=" * 55)
print("  ARRAYS")
print("=" * 55)


# 1. Find maximum and minimum in an array
def find_min_max(arr):
    if not arr: return None, None
    mn, mx = arr[0], arr[0]
    for x in arr[1:]:
        if x < mn: mn = x
        if x > mx: mx = x
    return mn, mx

arr = [3, 7, 1, 9, 4, 6, 2]
mn, mx = find_min_max(arr)
print(f"\n1. Min/Max of {arr}:")
print(f"   Min = {mn}, Max = {mx}")


# 2. Reverse an array in-place
def reverse_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1; right -= 1
    return arr

arr2 = [1, 2, 3, 4, 5]
print(f"\n2. Reverse {arr2}:")
print(f"   Result: {reverse_array(arr2.copy())}")


# 3. Find duplicate elements
def find_duplicates(arr):
    seen, dupes = set(), set()
    for x in arr:
        if x in seen: dupes.add(x)
        else: seen.add(x)
    return sorted(dupes)

arr3 = [1, 3, 4, 2, 2, 3, 7]
print(f"\n3. Duplicates in {arr3}:")
print(f"   Duplicates: {find_duplicates(arr3)}")


# 4. Two Sum — find indices of two numbers that add to target
def two_sum(arr, target):
    """Return indices of two elements that sum to target. O(n)"""
    seen = {}           # value → index
    for i, x in enumerate(arr):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None

arr4 = [2, 7, 11, 15]
result = two_sum(arr4, 9)
print(f"\n4. Two Sum: {arr4}, target=9")
print(f"   Indices: {result}  → values: {arr4[result[0]]}, {arr4[result[1]]}")


# 5. Move all zeros to the end
def move_zeros(arr):
    pos = 0
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[pos], arr[i] = arr[i], arr[pos]
            pos += 1
    return arr

arr5 = [0, 1, 0, 3, 12, 0, 5]
print(f"\n5. Move Zeros: {arr5}")
print(f"   Result: {move_zeros(arr5.copy())}")


# 6. Maximum subarray sum (Kadane's Algorithm)
def max_subarray(arr):
    """Kadane's Algorithm — O(n)"""
    max_sum = current = arr[0]
    start = end = temp_start = 0
    for i in range(1, len(arr)):
        if arr[i] > current + arr[i]:
            current = arr[i]
            temp_start = i
        else:
            current += arr[i]
        if current > max_sum:
            max_sum = current
            start, end = temp_start, i
    return max_sum, arr[start:end+1]

arr6 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_sum, subarray = max_subarray(arr6)
print(f"\n6. Max Subarray Sum: {arr6}")
print(f"   Max sum = {max_sum}, subarray = {subarray}")


# 7. Rotate array by k positions
def rotate_array(arr, k):
    n = len(arr)
    k = k % n
    return arr[n-k:] + arr[:n-k]

arr7 = [1, 2, 3, 4, 5, 6, 7]
print(f"\n7. Rotate {arr7} by 3:")
print(f"   Result: {rotate_array(arr7, 3)}")


# 8. Find missing number in 0..n
def missing_number(arr):
    n = len(arr)
    return n * (n + 1) // 2 - sum(arr)

arr8 = [3, 0, 1]
print(f"\n8. Missing number in {arr8}: {missing_number(arr8)}")


# 9. Remove duplicates from sorted array (in-place)
def remove_sorted_duplicates(arr):
    if not arr: return 0
    k = 1
    for i in range(1, len(arr)):
        if arr[i] != arr[i-1]:
            arr[k] = arr[i]
            k += 1
    return arr[:k]

arr9 = [1, 1, 2, 2, 3, 4, 4, 5]
print(f"\n9. Remove duplicates from sorted {arr9}:")
print(f"   Result: {remove_sorted_duplicates(arr9.copy())}")


# 10. Merge two sorted arrays
def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]: result.append(a[i]); i += 1
        else: result.append(b[j]); j += 1
    return result + a[i:] + b[j:]

a = [1, 3, 5, 7]; b = [2, 4, 6, 8]
print(f"\n10. Merge sorted {a} + {b}:")
print(f"    Result: {merge_sorted(a, b)}")


# ────────────────────────────────────────────────────────────
#  STRINGS
# ────────────────────────────────────────────────────────────

print("\n" + "="*55)
print("  STRINGS")
print("="*55)


# 1. Check palindrome
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

for w in ["racecar", "hello", "A man a plan a canal Panama"]:
    print(f"\n1. Is '{w}' a palindrome? {is_palindrome(w)}")


# 2. Count vowels and consonants
def count_vowels_consonants(s):
    vowels = "aeiouAEIOU"
    v = sum(1 for c in s if c in vowels)
    c = sum(1 for c in s if c.isalpha() and c not in vowels)
    return v, c

s2 = "Hello Python"
v, c = count_vowels_consonants(s2)
print(f"\n2. '{s2}': Vowels={v}, Consonants={c}")


# 3. Reverse words in a sentence
def reverse_words(s):
    return " ".join(s.split()[::-1])

s3 = "Hello World from Python"
print(f"\n3. Reverse words: '{s3}'")
print(f"   Result: '{reverse_words(s3)}'")


# 4. Check anagram
def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

pairs = [("listen", "silent"), ("hello", "world"), ("Astronomer", "Moon starer")]
for a, b in pairs:
    print(f"\n4. Anagram('{a}', '{b}')? {is_anagram(a, b)}")


# 5. Longest common prefix
def longest_common_prefix(words):
    if not words: return ""
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix: return ""
    return prefix

words = ["flower", "flow", "flight"]
print(f"\n5. LCP of {words}: '{longest_common_prefix(words)}'")


# 6. Count occurrences of each character
def char_frequency(s):
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: -x[1]))

s6 = "programming"
print(f"\n6. Char frequency of '{s6}': {char_frequency(s6)}")


# 7. First non-repeating character
def first_non_repeating(s):
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    for c in s:
        if freq[c] == 1:
            return c
    return None

s7 = "aabbcde"
print(f"\n7. First non-repeating in '{s7}': '{first_non_repeating(s7)}'")


# 8. Check if string has balanced brackets
def is_balanced(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in "({[": stack.append(c)
        elif c in ")}]":
            if not stack or stack[-1] != pairs[c]: return False
            stack.pop()
    return len(stack) == 0

for expr in ["(()[{}])", "([)]", "{{}}", "((("]:
    print(f"\n8. Balanced '{expr}'? {is_balanced(expr)}")


# 9. Compress a string (run-length encoding)
def compress(s):
    if not s: return ""
    result, count = s[0], 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]: count += 1
        else:
            result += str(count) if count > 1 else ""
            result += s[i]; count = 1
    result += str(count) if count > 1 else ""
    return result

s9 = "aaabbbccddddee"
print(f"\n9. Compress '{s9}': '{compress(s9)}'")


# 10. Find all permutations of a string
def permutations(s):
    if len(s) <= 1: return [s]
    result = []
    for i, c in enumerate(s):
        rest = s[:i] + s[i+1:]
        for perm in permutations(rest):
            result.append(c + perm)
    return sorted(set(result))

s10 = "abc"
perms = permutations(s10)
print(f"\n10. Permutations of '{s10}': {perms}")
