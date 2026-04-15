# ============================================================
#  Project 2: File-Based Notes App
#  Features: add, view, search, edit, delete notes
#            JSON persistence, timestamps, exception handling
# ============================================================

import json
import os
from datetime import datetime

NOTES_FILE = "notes_data.json"


# ────────────────────────────────────────────────────────────
#  FILE OPERATIONS
# ────────────────────────────────────────────────────────────

def load_notes():
    """Load notes from JSON file. Return empty list if file missing."""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ⚠️  Could not load notes: {e}. Starting fresh.")
        return []

def save_notes(notes):
    """Save notes list to JSON file."""
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=4)
    except IOError as e:
        print(f"  ❌ Could not save notes: {e}")


# ────────────────────────────────────────────────────────────
#  NOTE OPERATIONS
# ────────────────────────────────────────────────────────────

def add_note(notes):
    """Create a new note."""
    print("\n── ✏️  Add New Note ──────────────────")
    title = input("  Title: ").strip()
    if not title:
        print("  ❌ Title cannot be empty.")
        return

    print("  Content (press Enter twice to finish):")
    lines = []
    while True:
        line = input("  ")
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)

    content = "\n".join(lines).strip()
    if not content:
        print("  ❌ Content cannot be empty.")
        return

    note = {
        "id": len(notes) + 1,
        "title": title,
        "content": content,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    notes.append(note)
    save_notes(notes)
    print(f"  ✅ Note '{title}' added successfully!")


def view_all_notes(notes):
    """Display all notes as a list."""
    print("\n── 📋 All Notes ──────────────────────")
    if not notes:
        print("  📭 No notes yet. Add your first note!")
        return

    for note in notes:
        print(f"\n  [{note['id']}] 📝 {note['title']}")
        print(f"       Created : {note['created']}")
        print(f"       Updated : {note['updated']}")
        print(f"       Preview : {note['content'][:60]}{'...' if len(note['content']) > 60 else ''}")


def view_note(notes):
    """View full content of a single note."""
    view_all_notes(notes)
    if not notes:
        return

    try:
        note_id = int(input("\n  Enter note ID to view: "))
        note = next((n for n in notes if n["id"] == note_id), None)
        if not note:
            print("  ❌ Note not found.")
            return

        print("\n" + "=" * 45)
        print(f"  📝 {note['title']}")
        print(f"  Created: {note['created']}  |  Updated: {note['updated']}")
        print("─" * 45)
        print(note["content"])
        print("=" * 45)

    except ValueError:
        print("  ❌ Please enter a valid number.")


def search_notes(notes):
    """Search notes by keyword in title or content."""
    if not notes:
        print("\n  📭 No notes to search.")
        return

    keyword = input("\n  🔍 Enter search keyword: ").strip().lower()
    if not keyword:
        print("  ❌ Keyword cannot be empty.")
        return

    results = [
        n for n in notes
        if keyword in n["title"].lower() or keyword in n["content"].lower()
    ]

    if not results:
        print(f"  ❌ No notes found matching '{keyword}'.")
        return

    print(f"\n  Found {len(results)} result(s) for '{keyword}':")
    for note in results:
        # Highlight where keyword was found
        location = []
        if keyword in note["title"].lower():
            location.append("title")
        if keyword in note["content"].lower():
            location.append("content")
        print(f"\n  [{note['id']}] 📝 {note['title']}  (found in: {', '.join(location)})")
        print(f"       {note['content'][:80]}...")


def edit_note(notes):
    """Edit the title or content of an existing note."""
    view_all_notes(notes)
    if not notes:
        return

    try:
        note_id = int(input("\n  Enter note ID to edit: "))
        note = next((n for n in notes if n["id"] == note_id), None)
        if not note:
            print("  ❌ Note not found.")
            return

        print(f"\n  Editing: '{note['title']}'")
        print("  [1] Edit title  [2] Edit content  [3] Edit both  [0] Cancel")
        choice = input("  Choice: ").strip()

        if choice == "1" or choice == "3":
            new_title = input(f"  New title (current: '{note['title']}'): ").strip()
            if new_title:
                note["title"] = new_title

        if choice == "2" or choice == "3":
            print(f"  Current content:\n  {note['content']}\n")
            print("  New content (press Enter twice to finish):")
            lines = []
            while True:
                line = input("  ")
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            new_content = "\n".join(lines).strip()
            if new_content:
                note["content"] = new_content

        if choice in ("1", "2", "3"):
            note["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_notes(notes)
            print(f"  ✅ Note updated successfully!")
        else:
            print("  Cancelled.")

    except ValueError:
        print("  ❌ Please enter a valid number.")


def delete_note(notes):
    """Delete a note by ID."""
    view_all_notes(notes)
    if not notes:
        return

    try:
        note_id = int(input("\n  Enter note ID to delete: "))
        note = next((n for n in notes if n["id"] == note_id), None)
        if not note:
            print("  ❌ Note not found.")
            return

        confirm = input(f"  ⚠️  Delete '{note['title']}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            notes.remove(note)
            # Re-number remaining notes
            for i, n in enumerate(notes, 1):
                n["id"] = i
            save_notes(notes)
            print(f"  ✅ Note '{note['title']}' deleted.")
        else:
            print("  Cancelled.")

    except ValueError:
        print("  ❌ Please enter a valid number.")


def export_notes(notes):
    """Export all notes to a plain .txt file."""
    if not notes:
        print("  ❌ No notes to export.")
        return

    filename = f"notes_export_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    try:
        with open(filename, "w") as f:
            f.write("=" * 50 + "\n")
            f.write("         MY NOTES EXPORT\n")
            f.write(f"   Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 50 + "\n\n")
            for note in notes:
                f.write(f"[{note['id']}] {note['title']}\n")
                f.write(f"Created: {note['created']} | Updated: {note['updated']}\n")
                f.write("-" * 40 + "\n")
                f.write(note["content"] + "\n\n")
        print(f"  ✅ Notes exported to '{filename}'")
    except IOError as e:
        print(f"  ❌ Export failed: {e}")


# ────────────────────────────────────────────────────────────
#  MENU
# ────────────────────────────────────────────────────────────

def display_menu(total):
    print("\n" + "=" * 42)
    print(f"     📓  NOTES APP  ({total} note(s))")
    print("=" * 42)
    print("  [1]  Add New Note")
    print("  [2]  View All Notes")
    print("  [3]  Read a Note")
    print("  [4]  Search Notes")
    print("  [5]  Edit a Note")
    print("  [6]  Delete a Note")
    print("  [7]  Export to .txt File")
    print("  [0]  Exit")
    print("=" * 42)


def main():
    print("\n  Welcome to your Notes App! 📓")
    notes = load_notes()
    print(f"  Loaded {len(notes)} saved note(s).")

    while True:
        display_menu(len(notes))
        choice = input("  Enter choice: ").strip()

        if   choice == "1": add_note(notes)
        elif choice == "2": view_all_notes(notes)
        elif choice == "3": view_note(notes)
        elif choice == "4": search_notes(notes)
        elif choice == "5": edit_note(notes)
        elif choice == "6": delete_note(notes)
        elif choice == "7": export_notes(notes)
        elif choice == "0":
            print("\n  👋 Goodbye! Your notes are saved.")
            break
        else:
            print("  ⚠️  Invalid choice. Please try again.")


# ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
