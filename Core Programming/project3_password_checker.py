# ============================================================
#  PHASE 2 — Project 3: Password Checker & Generator
#  Features: strength analysis, detailed feedback, password
#            generator, save history to file, exception handling
# ============================================================

import random
import string
import re
import json
import os
from datetime import datetime

HISTORY_FILE = "password_history.json"


# ────────────────────────────────────────────────────────────
#  PASSWORD STRENGTH CHECKER
# ────────────────────────────────────────────────────────────

# Common weak passwords to warn against
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "111111", "iloveyou", "admin", "letmein",
    "welcome", "monkey", "dragon", "master", "sunshine",
    "princess", "password123", "123456789", "1234567890",
}

def check_password_strength(password):
    """
    Analyse a password and return a score, grade, and feedback.
    Returns: (score, grade, label, feedback_list, suggestions_list)
    """
    score = 0
    feedback = []
    suggestions = []

    # ── 1. Length ─────────────────────────────────────────
    length = len(password)
    if length == 0:
        return 0, "F", "Empty", ["Password is empty."], ["Please enter a password."]

    if length >= 16:
        score += 3
        feedback.append(f"✅ Length is excellent ({length} characters)")
    elif length >= 12:
        score += 2
        feedback.append(f"✅ Length is good ({length} characters)")
    elif length >= 8:
        score += 1
        feedback.append(f"⚠️  Length is acceptable ({length} characters)")
    else:
        feedback.append(f"❌ Too short ({length} characters)")
        suggestions.append("Use at least 8 characters (12+ is recommended)")

    # ── 2. Uppercase letters ──────────────────────────────
    if re.search(r"[A-Z]", password):
        score += 1
        feedback.append("✅ Contains uppercase letters")
    else:
        feedback.append("❌ No uppercase letters")
        suggestions.append("Add uppercase letters (A–Z)")

    # ── 3. Lowercase letters ──────────────────────────────
    if re.search(r"[a-z]", password):
        score += 1
        feedback.append("✅ Contains lowercase letters")
    else:
        feedback.append("❌ No lowercase letters")
        suggestions.append("Add lowercase letters (a–z)")

    # ── 4. Digits ─────────────────────────────────────────
    digit_count = len(re.findall(r"\d", password))
    if digit_count >= 2:
        score += 2
        feedback.append(f"✅ Contains numbers ({digit_count} digits)")
    elif digit_count == 1:
        score += 1
        feedback.append("⚠️  Only 1 digit — add more")
        suggestions.append("Include at least 2 digits")
    else:
        feedback.append("❌ No digits")
        suggestions.append("Add numbers (0–9)")

    # ── 5. Special characters ─────────────────────────────
    special_chars = re.findall(r"[!@#$%^&*()\-_=+\[\]{}|;:,.<>?/~`]", password)
    if len(special_chars) >= 2:
        score += 2
        feedback.append(f"✅ Contains special characters ({len(special_chars)} found)")
    elif len(special_chars) == 1:
        score += 1
        feedback.append("⚠️  Only 1 special character")
        suggestions.append("Add more special characters (!@#$% etc.)")
    else:
        feedback.append("❌ No special characters")
        suggestions.append("Add special characters like !@#$%^&*")

    # ── 6. No repeated characters ─────────────────────────
    if re.search(r"(.)\1{2,}", password):
        score -= 1
        feedback.append("⚠️  Has 3+ repeated characters in a row")
        suggestions.append("Avoid repeating the same character many times")
    else:
        feedback.append("✅ No excessive repeated characters")

    # ── 7. No sequential patterns ─────────────────────────
    sequences = ["123456789", "987654321", "abcdefgh", "qwerty", "asdfgh"]
    has_sequence = any(seq in password.lower() for seq in sequences)
    if has_sequence:
        score -= 1
        feedback.append("⚠️  Contains a common sequence (e.g. 123, qwerty)")
        suggestions.append("Avoid common sequences like '1234' or 'qwerty'")
    else:
        feedback.append("✅ No common keyboard/number sequences")

    # ── 8. Common password check ──────────────────────────
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append("🚨 This is one of the most common passwords!")
        suggestions.insert(0, "Do NOT use this password — it is on every hacker's list!")

    # ── Grade ─────────────────────────────────────────────
    score = max(0, score)   # no negative scores
    if score >= 9:
        grade, label = "A+", "Very Strong 💪"
    elif score >= 7:
        grade, label = "A",  "Strong 👍"
    elif score >= 5:
        grade, label = "B",  "Moderate ⚠️"
    elif score >= 3:
        grade, label = "C",  "Weak 😬"
    else:
        grade, label = "F",  "Very Weak 🚨"

    return score, grade, label, feedback, suggestions


def display_result(password, score, grade, label, feedback, suggestions):
    """Pretty-print the strength analysis."""
    print("\n" + "═" * 48)
    print(f"  🔐 Password Analysis")
    print("═" * 48)
    print(f"  Password  : {'*' * len(password)}  ({len(password)} chars)")
    print(f"  Score     : {score}/10")
    print(f"  Grade     : {grade}  —  {label}")
    print()

    # Visual strength bar
    filled = int((score / 10) * 20)
    bar_color = "█" * filled + "░" * (20 - filled)
    print(f"  Strength  : [{bar_color}] {score}/10")
    print()

    print("  📋 Detailed Feedback:")
    for item in feedback:
        print(f"     {item}")

    if suggestions:
        print("\n  💡 Suggestions to Improve:")
        for tip in suggestions:
            print(f"     → {tip}")

    print("═" * 48)


# ────────────────────────────────────────────────────────────
#  PASSWORD GENERATOR
# ────────────────────────────────────────────────────────────

def generate_password(length=16, use_upper=True, use_digits=True,
                       use_symbols=True, avoid_ambiguous=False):
    """
    Generate a secure random password.
    Guarantees at least one character from each enabled category.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    chars = string.ascii_lowercase
    required = [random.choice(string.ascii_lowercase)]

    if use_upper:
        pool = string.ascii_uppercase
        if avoid_ambiguous:
            pool = pool.replace("I", "").replace("O", "")
        chars += pool
        required.append(random.choice(pool))

    if use_digits:
        pool = string.digits
        if avoid_ambiguous:
            pool = pool.replace("0", "").replace("1", "")
        chars += pool
        required.append(random.choice(pool))

    if use_symbols:
        pool = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        chars += pool
        required.append(random.choice(pool))

    if avoid_ambiguous:
        chars = chars.replace("I","").replace("O","").replace("0","").replace("1","").replace("l","")

    remaining = random.choices(chars, k=max(0, length - len(required)))
    password_chars = required + remaining
    random.shuffle(password_chars)
    return "".join(password_chars)


# ────────────────────────────────────────────────────────────
#  HISTORY MANAGEMENT
# ────────────────────────────────────────────────────────────

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_to_history(password, score, grade, label):
    history = load_history()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "password_masked": "*" * len(password),
        "length": len(password),
        "score": score,
        "grade": grade,
        "strength": label,
    }
    history.append(entry)
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
    except IOError as e:
        print(f"  ⚠️  Could not save history: {e}")

def show_history():
    history = load_history()
    if not history:
        print("\n  📭 No check history yet.")
        return
    print("\n  📋 Password Check History:")
    print(f"  {'#':<4} {'Time':<22} {'Length':<8} {'Score':<8} {'Grade':<6} Strength")
    print("  " + "─" * 60)
    for i, h in enumerate(history[-15:], 1):  # Show last 15
        print(f"  {i:<4} {h['timestamp']:<22} {h['length']:<8} "
              f"{h['score']}/10   {h['grade']:<6} {h['strength']}")


# ────────────────────────────────────────────────────────────
#  MENU
# ────────────────────────────────────────────────────────────

def check_password_menu():
    """Check the strength of a user-entered password."""
    import getpass
    try:
        # Try to hide password input (works in most terminals)
        password = getpass.getpass("\n  Enter password to check (hidden): ")
    except Exception:
        password = input("\n  Enter password to check: ")

    if not password:
        print("  ❌ No password entered.")
        return

    score, grade, label, feedback, suggestions = check_password_strength(password)
    display_result(password, score, grade, label, feedback, suggestions)

    save = input("\n  Save result to history? (y/n): ").strip().lower()
    if save == "y":
        save_to_history(password, score, grade, label)
        print("  ✅ Saved to history.")


def generate_password_menu():
    """Interactively generate a strong password."""
    print("\n── 🔧 Password Generator ────────────────")
    try:
        length = int(input("  Length (default 16): ").strip() or 16)
        if length < 4 or length > 128:
            raise ValueError("Length must be 4–128.")
    except ValueError as e:
        print(f"  ❌ {e}")
        return

    upper   = input("  Include uppercase? (Y/n): ").strip().lower() not in ("n","no")
    digits  = input("  Include digits?    (Y/n): ").strip().lower() not in ("n","no")
    symbols = input("  Include symbols?   (Y/n): ").strip().lower() not in ("n","no")
    avoid   = input("  Avoid ambiguous chars (0,O,l,I)? (y/N): ").strip().lower() in ("y","yes")

    count = int(input("  How many to generate? (default 5): ").strip() or 5)

    print(f"\n  🔑 Generated Passwords:")
    print("  " + "─" * 40)
    for i in range(1, count + 1):
        pw = generate_password(length, upper, digits, symbols, avoid)
        score, grade, label, _, _ = check_password_strength(pw)
        print(f"  {i}.  {pw}   [{grade} — {label}]")
    print("  " + "─" * 40)


def display_menu():
    print("\n" + "=" * 42)
    print("    🔐  PASSWORD CHECKER & GENERATOR")
    print("=" * 42)
    print("  [1]  Check Password Strength")
    print("  [2]  Generate Strong Password")
    print("  [3]  View Check History")
    print("  [0]  Exit")
    print("=" * 42)


def main():
    print("\n  Welcome to the Password Tool! 🔐")
    print("  Keep your accounts safe with strong passwords.\n")

    while True:
        display_menu()
        choice = input("  Enter choice: ").strip()

        if   choice == "1": check_password_menu()
        elif choice == "2": generate_password_menu()
        elif choice == "3": show_history()
        elif choice == "0":
            print("\n  👋 Stay safe and use strong passwords!")
            break
        else:
            print("  ⚠️  Invalid choice.")


# ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
