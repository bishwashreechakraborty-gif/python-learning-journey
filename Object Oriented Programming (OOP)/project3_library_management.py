# ============================================================
#  Project 3: Library Management System
#  OOP Concepts: All 4 pillars, ABC, @property, JSON storage
# ============================================================

import json, os
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

DATA_FILE = "library_db.json"
FINE_PER_DAY = 5.0   # ₹5 per day overdue


# ────────────────────────────────────────────────────────────
#  BASE LIBRARY ITEM (Abstract)
# ────────────────────────────────────────────────────────────

class LibraryItem(ABC):
    _id_counter = 1

    def __init__(self, title, author, year):
        self._item_id  = f"LIB{LibraryItem._id_counter:04d}"
        self._title    = title
        self._author   = author
        self._year     = year
        self._available= True
        self._borrowed_by   = None
        self._due_date      = None
        LibraryItem._id_counter += 1

    @property
    def item_id(self):   return self._item_id
    @property
    def title(self):     return self._title
    @property
    def author(self):    return self._author
    @property
    def available(self): return self._available

    @abstractmethod
    def item_type(self): pass

    @abstractmethod
    def borrow_period(self): pass   # days

    def borrow(self, member_id):
        if not self._available:
            print(f"  ❌ '{self._title}' is currently unavailable.")
            return False
        self._available  = False
        self._borrowed_by = member_id
        self._due_date   = (datetime.now() + timedelta(days=self.borrow_period())).strftime("%Y-%m-%d")
        print(f"  ✅ '{self._title}' borrowed. Due: {self._due_date}")
        return True

    def return_item(self):
        if self._available:
            print(f"  ⚠️  '{self._title}' wasn't borrowed.")
            return 0.0
        fine = self._calculate_fine()
        self._available   = True
        self._borrowed_by = None
        self._due_date    = None
        if fine > 0:
            print(f"  ✅ Returned. Fine due: ₹{fine:.2f}")
        else:
            print(f"  ✅ '{self._title}' returned on time.")
        return fine

    def _calculate_fine(self):
        if not self._due_date: return 0.0
        due = datetime.strptime(self._due_date, "%Y-%m-%d")
        overdue_days = (datetime.now() - due).days
        return max(0, overdue_days * FINE_PER_DAY)

    def __str__(self):
        status = "📗 Available" if self._available else f"📕 Out (due {self._due_date})"
        return (f"[{self._item_id}] {self._title:<30} "
                f"{self._author:<20} {self._year}  {status}")

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "item_id": self._item_id, "title": self._title,
            "author": self._author, "year": self._year,
            "available": self._available, "borrowed_by": self._borrowed_by,
            "due_date": self._due_date,
            **self._extra_dict(),
        }

    def _extra_dict(self): return {}


# ────────────────────────────────────────────────────────────
#  ITEM TYPES (Polymorphism)
# ────────────────────────────────────────────────────────────

class Book(LibraryItem):
    def __init__(self, title, author, year, genre="General", pages=0):
        super().__init__(title, author, year)
        self.__genre = genre
        self.__pages = pages

    def item_type(self):    return "Book 📚"
    def borrow_period(self): return 14   # 2 weeks

    def _extra_dict(self):
        return {"genre": self.__genre, "pages": self.__pages}

    def __str__(self):
        return super().__str__() + f"  [{self.__genre}]"


class Magazine(LibraryItem):
    def __init__(self, title, author, year, issue_number):
        super().__init__(title, author, year)
        self.__issue = issue_number

    def item_type(self):     return "Magazine 📰"
    def borrow_period(self): return 7   # 1 week

    def _extra_dict(self):
        return {"issue_number": self.__issue}

    def __str__(self):
        return super().__str__() + f"  [Issue #{self.__issue}]"


class DVD(LibraryItem):
    def __init__(self, title, author, year, duration_mins):
        super().__init__(title, author, year)
        self.__duration = duration_mins

    def item_type(self):     return "DVD 💿"
    def borrow_period(self): return 3   # 3 days

    def _extra_dict(self):
        return {"duration_mins": self.__duration}

    def __str__(self):
        return super().__str__() + f"  [{self.__duration} min]"


# ────────────────────────────────────────────────────────────
#  MEMBER CLASS
# ────────────────────────────────────────────────────────────

class Member:
    _m_counter = 1

    def __init__(self, name, email, phone):
        self.__member_id = f"MEM{Member._m_counter:04d}"
        self.__name      = name
        self.__email     = email
        self.__phone     = phone
        self.__borrowed  = []       # list of item_ids
        self.__fines     = 0.0
        self.__joined    = datetime.now().strftime("%Y-%m-%d")
        Member._m_counter += 1

    @property
    def member_id(self): return self.__member_id
    @property
    def name(self):      return self.__name
    @property
    def fines(self):     return self.__fines

    def add_borrowed(self, item_id):
        self.__borrowed.append(item_id)

    def remove_borrowed(self, item_id):
        if item_id in self.__borrowed:
            self.__borrowed.remove(item_id)

    def add_fine(self, amount):
        self.__fines += amount

    def pay_fine(self, amount):
        if amount > self.__fines:
            amount = self.__fines
        self.__fines -= amount
        print(f"  ✅ ₹{amount:.2f} paid. Remaining fine: ₹{self.__fines:.2f}")

    def __str__(self):
        borrowed_count = len(self.__borrowed)
        fine_str = f"  Fine: ₹{self.__fines:.2f}" if self.__fines > 0 else ""
        return (f"[{self.__member_id}] {self.__name:<20} "
                f"{self.__email:<25} Borrowed: {borrowed_count}{fine_str}")

    def profile(self):
        return (f"\n  {'─'*45}\n"
                f"  Member ID : {self.__member_id}\n"
                f"  Name      : {self.__name}\n"
                f"  Email     : {self.__email}\n"
                f"  Phone     : {self.__phone}\n"
                f"  Joined    : {self.__joined}\n"
                f"  Borrowed  : {self.__borrowed}\n"
                f"  Fines     : ₹{self.__fines:.2f}\n"
                f"  {'─'*45}")

    def to_dict(self):
        return {
            "member_id": self.__member_id, "name": self.__name,
            "email": self.__email, "phone": self.__phone,
            "borrowed": self.__borrowed, "fines": self.__fines,
            "joined": self.__joined,
        }

    @classmethod
    def from_dict(cls, d):
        obj = cls.__new__(cls)
        obj._Member__member_id = d["member_id"]
        obj._Member__name      = d["name"]
        obj._Member__email     = d["email"]
        obj._Member__phone     = d["phone"]
        obj._Member__borrowed  = d.get("borrowed", [])
        obj._Member__fines     = d.get("fines", 0.0)
        obj._Member__joined    = d.get("joined", "N/A")
        return obj


# ────────────────────────────────────────────────────────────
#  LIBRARY SYSTEM
# ────────────────────────────────────────────────────────────

class Library:
    def __init__(self, name="City Library"):
        self.name    = name
        self.__items   = {}     # item_id → LibraryItem
        self.__members = {}     # member_id → Member
        self.__load()

    def __load(self):
        if not os.path.exists(DATA_FILE): return
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
            type_map = {"Book": Book, "Magazine": Magazine, "DVD": DVD}
            for d in data.get("items", []):
                cls = type_map.get(d["type"])
                if cls:
                    item = cls.__new__(cls)
                    item._item_id     = d["item_id"]
                    item._title       = d["title"]
                    item._author      = d["author"]
                    item._year        = d["year"]
                    item._available   = d["available"]
                    item._borrowed_by = d["borrowed_by"]
                    item._due_date    = d["due_date"]
                    if cls == Book:
                        item._Book__genre = d.get("genre", "General")
                        item._Book__pages = d.get("pages", 0)
                    elif cls == Magazine:
                        item._Magazine__issue = d.get("issue_number", 0)
                    elif cls == DVD:
                        item._DVD__duration = d.get("duration_mins", 0)
                    self.__items[item.item_id] = item
            for d in data.get("members", []):
                m = Member.from_dict(d)
                self.__members[m.member_id] = m
            if self.__items:
                max_id = max(int(k[3:]) for k in self.__items)
                LibraryItem._id_counter = max_id + 1
            if self.__members:
                max_mid = max(int(k[3:]) for k in self.__members)
                Member._m_counter = max_mid + 1
            print(f"  📂 Loaded {len(self.__items)} item(s), {len(self.__members)} member(s).")
        except Exception as e:
            print(f"  ⚠️  Load error: {e}")

    def __save(self):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "items":   [i.to_dict() for i in self.__items.values()],
                "members": [m.to_dict() for m in self.__members.values()],
            }, f, indent=2)

    def __get_item(self, item_id):
        item = self.__items.get(item_id.upper())
        if not item: print("  ❌ Item not found.")
        return item

    def __get_member(self, member_id):
        m = self.__members.get(member_id.upper())
        if not m: print("  ❌ Member not found.")
        return m

    # ── Add items ─────────────────────────────────────────
    def add_book(self):
        print("\n── ➕ Add Book ───────────────────────")
        title  = input("  Title  : ")
        author = input("  Author : ")
        year   = int(input("  Year   : "))
        genre  = input("  Genre  : ")
        pages  = int(input("  Pages  : ") or 0)
        item = Book(title, author, year, genre, pages)
        self.__items[item.item_id] = item
        self.__save()
        print(f"  ✅ Book added. ID: {item.item_id}")

    def add_magazine(self):
        print("\n── ➕ Add Magazine ───────────────────")
        title  = input("  Title   : ")
        author = input("  Publisher: ")
        year   = int(input("  Year    : "))
        issue  = int(input("  Issue # : "))
        item = Magazine(title, author, year, issue)
        self.__items[item.item_id] = item
        self.__save()
        print(f"  ✅ Magazine added. ID: {item.item_id}")

    def add_dvd(self):
        print("\n── ➕ Add DVD ────────────────────────")
        title    = input("  Title    : ")
        director = input("  Director : ")
        year     = int(input("  Year     : "))
        duration = int(input("  Duration (mins): "))
        item = DVD(title, director, year, duration)
        self.__items[item.item_id] = item
        self.__save()
        print(f"  ✅ DVD added. ID: {item.item_id}")

    # ── Members ───────────────────────────────────────────
    def register_member(self):
        print("\n── 👤 Register Member ───────────────")
        name  = input("  Name  : ")
        email = input("  Email : ")
        phone = input("  Phone : ")
        m = Member(name, email, phone)
        self.__members[m.member_id] = m
        self.__save()
        print(f"  ✅ Member registered. ID: {m.member_id}")

    # ── Borrow & Return ───────────────────────────────────
    def borrow_item(self):
        print("\n── 📤 Borrow Item ───────────────────")
        mid = input("  Member ID : ").upper()
        iid = input("  Item ID   : ").upper()
        member = self.__get_member(mid)
        item   = self.__get_item(iid)
        if member and item:
            if item.borrow(mid):
                member.add_borrowed(iid)
                self.__save()

    def return_item(self):
        print("\n── 📥 Return Item ────────────────────")
        mid = input("  Member ID : ").upper()
        iid = input("  Item ID   : ").upper()
        member = self.__get_member(mid)
        item   = self.__get_item(iid)
        if member and item:
            fine = item.return_item()
            member.remove_borrowed(iid)
            if fine > 0:
                member.add_fine(fine)
            self.__save()

    # ── View / Search ─────────────────────────────────────
    def list_items(self):
        print(f"\n── 📚 All Items ({len(self.__items)}) ──────────────────")
        for item in self.__items.values():
            print(f"  {item}")

    def list_members(self):
        print(f"\n── 👥 All Members ({len(self.__members)}) ────────────────")
        for m in self.__members.values():
            print(f"  {m}")

    def search(self):
        keyword = input("\n  Search (title/author/type): ").lower()
        results = [i for i in self.__items.values()
                   if keyword in i.title.lower() or keyword in i.author.lower()
                   or keyword in i.item_type().lower()]
        print(f"  Found {len(results)} result(s):")
        for i in results:
            print(f"  {i}")

    def member_profile(self):
        mid = input("\n  Member ID: ").upper()
        m = self.__get_member(mid)
        if m: print(m.profile())

    def pay_fine(self):
        mid = input("\n  Member ID: ").upper()
        m = self.__get_member(mid)
        if not m: return
        if m.fines == 0:
            print("  ✅ No fines pending.")
            return
        print(f"  Outstanding fine: ₹{m.fines:.2f}")
        amount = float(input("  Amount to pay: ₹"))
        m.pay_fine(amount)
        self.__save()

    def statistics(self):
        total  = len(self.__items)
        avail  = sum(1 for i in self.__items.values() if i.available)
        books  = sum(1 for i in self.__items.values() if isinstance(i, Book))
        mags   = sum(1 for i in self.__items.values() if isinstance(i, Magazine))
        dvds   = sum(1 for i in self.__items.values() if isinstance(i, DVD))
        fines  = sum(m.fines for m in self.__members.values())
        print(f"\n  📊 Library Statistics")
        print(f"  {'─'*35}")
        print(f"  Total Items    : {total}  (Available: {avail}, Out: {total-avail})")
        print(f"  Books          : {books}")
        print(f"  Magazines      : {mags}")
        print(f"  DVDs           : {dvds}")
        print(f"  Members        : {len(self.__members)}")
        print(f"  Total Fines    : ₹{fines:.2f}")

    def run(self):
        print(f"\n  Welcome to {self.name} 📚")
        menu = [
            ("1",  "Add Book",          self.add_book),
            ("2",  "Add Magazine",      self.add_magazine),
            ("3",  "Add DVD",           self.add_dvd),
            ("4",  "Register Member",   self.register_member),
            ("5",  "Borrow Item",       self.borrow_item),
            ("6",  "Return Item",       self.return_item),
            ("7",  "All Items",         self.list_items),
            ("8",  "All Members",       self.list_members),
            ("9",  "Search Items",      self.search),
            ("10", "Member Profile",    self.member_profile),
            ("11", "Pay Fine",          self.pay_fine),
            ("12", "Statistics",        self.statistics),
            ("0",  "Exit",              None),
        ]
        while True:
            print(f"\n{'═'*35}  {self.name}")
            for k, label, _ in menu:
                print(f"  [{k:>2}] {label}")
            choice = input("  Choice: ").strip()
            if choice == "0":
                print("\n  📚 Goodbye! Happy reading!")
                break
            match = next((fn for k,_,fn in menu if k == choice), None)
            if match:
                try: match()
                except (ValueError, TypeError) as e: print(f"  ❌ {e}")
            else:
                print("  ⚠️  Invalid choice.")

if __name__ == "__main__":
    Library("City Library 📚").run()
