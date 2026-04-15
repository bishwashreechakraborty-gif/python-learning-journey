# ============================================================
#  Project 1: Student Management System
#  OOP Concepts used: Classes, Inheritance, Encapsulation,
#  Polymorphism, File Persistence (JSON)
# ============================================================

import json, os
from datetime import datetime

DATA_FILE = "students_db.json"

# ────────────────────────────────────────────────────────────
#  BASE PERSON CLASS
# ────────────────────────────────────────────────────────────

class Person:
    def __init__(self, name, age, email):
        self._name  = name
        self._age   = age
        self._email = email

    @property
    def name(self):  return self._name
    @property
    def age(self):   return self._age
    @property
    def email(self): return self._email

    def get_info(self):
        return f"Name: {self._name} | Age: {self._age} | Email: {self._email}"

    def __str__(self):
        return f"{self.__class__.__name__}: {self._name}"


# ────────────────────────────────────────────────────────────
#  STUDENT CLASS
# ────────────────────────────────────────────────────────────

class Student(Person):
    _id_counter = 1

    def __init__(self, name, age, email, course):
        super().__init__(name, age, email)
        self.__id      = f"STU{Student._id_counter:04d}"
        self.__course  = course
        self.__grades  = {}           # subject → score
        self.__enrolled = datetime.now().strftime("%Y-%m-%d")
        Student._id_counter += 1

    @property
    def student_id(self): return self.__id
    @property
    def course(self):     return self.__course
    @property
    def grades(self):     return dict(self.__grades)
    @property
    def enrolled(self):   return self.__enrolled

    def add_grade(self, subject, score):
        if not (0 <= score <= 100):
            raise ValueError(f"Score must be 0–100, got {score}")
        self.__grades[subject] = score
        print(f"  ✅ {subject}: {score} added for {self._name}")

    def average(self):
        if not self.__grades:
            return 0.0
        return sum(self.__grades.values()) / len(self.__grades)

    def letter_grade(self):
        avg = self.average()
        if avg >= 90: return "A+"
        if avg >= 80: return "A"
        if avg >= 70: return "B"
        if avg >= 60: return "C"
        if avg >= 50: return "D"
        return "F"

    def status(self):
        return "Pass ✅" if self.average() >= 50 else "Fail ❌"

    def report_card(self):
        lines = [
            f"  ╔{'═'*38}╗",
            f"  ║   REPORT CARD                       ║",
            f"  ╠{'═'*38}╣",
            f"  ║  ID     : {self.__id:<27}║",
            f"  ║  Name   : {self._name:<27}║",
            f"  ║  Course : {self.__course:<27}║",
            f"  ║  Enrolled: {self.__enrolled:<26}║",
            f"  ╠{'═'*38}╣",
            f"  ║  {'Subject':<18} {'Score':>5}  {'Grade':>5} ║",
            f"  ║  {'─'*35} ║",
        ]
        for subject, score in self.__grades.items():
            lg = "A+" if score>=90 else "A" if score>=80 else "B" if score>=70 else "C" if score>=60 else "D" if score>=50 else "F"
            lines.append(f"  ║  {subject:<18} {score:>5}  {lg:>5} ║")
        lines += [
            f"  ╠{'═'*38}╣",
            f"  ║  Average : {self.average():>5.1f}  Grade: {self.letter_grade():<9}   ║",
            f"  ║  Status  : {self.status():<27}║",
            f"  ╚{'═'*38}╝",
        ]
        return "\n".join(lines)

    def to_dict(self):
        return {
            "id": self.__id, "name": self._name, "age": self._age,
            "email": self._email, "course": self.__course,
            "grades": self.__grades, "enrolled": self.__enrolled,
        }

    @classmethod
    def from_dict(cls, data):
        s = cls.__new__(cls)
        Person.__init__(s, data["name"], data["age"], data["email"])
        s._Student__id       = data["id"]
        s._Student__course   = data["course"]
        s._Student__grades   = data.get("grades", {})
        s._Student__enrolled = data.get("enrolled", "N/A")
        return s

    def __str__(self):
        return (f"[{self.__id}] {self._name} | {self.__course} | "
                f"Avg: {self.average():.1f} ({self.letter_grade()}) | {self.status()}")


# ────────────────────────────────────────────────────────────
#  SYSTEM CLASS
# ────────────────────────────────────────────────────────────

class StudentManagementSystem:
    def __init__(self):
        self.__students = []
        self.__load()

    def __load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE) as f:
                    data = json.load(f)
                self.__students = [Student.from_dict(d) for d in data]
                if self.__students:
                    max_id = max(int(s.student_id[3:]) for s in self.__students)
                    Student._id_counter = max_id + 1
                print(f"  📂 Loaded {len(self.__students)} student(s) from file.")
            except Exception as e:
                print(f"  ⚠️  Load error: {e}")

    def __save(self):
        with open(DATA_FILE, "w") as f:
            json.dump([s.to_dict() for s in self.__students], f, indent=2)

    def __find(self, student_id):
        return next((s for s in self.__students if s.student_id == student_id), None)

    # ── CRUD ──────────────────────────────────────────────
    def add_student(self):
        print("\n── ➕ Add Student ───────────────────")
        try:
            name   = input("  Full Name  : ").strip()
            age    = int(input("  Age        : "))
            email  = input("  Email      : ").strip()
            course = input("  Course     : ").strip()
            s = Student(name, age, email, course)
            self.__students.append(s)
            self.__save()
            print(f"  ✅ Student added! ID: {s.student_id}")
        except ValueError as e:
            print(f"  ❌ {e}")

    def view_all(self):
        print("\n── 📋 All Students ──────────────────")
        if not self.__students:
            print("  No students enrolled yet.")
            return
        for s in self.__students:
            print(f"  {s}")

    def view_student(self):
        sid = input("\n  Enter Student ID: ").strip().upper()
        s = self.__find(sid)
        if not s:
            print("  ❌ Student not found.")
            return
        print(s.report_card())

    def add_grade(self):
        print("\n── 📝 Add Grade ─────────────────────")
        sid     = input("  Student ID : ").strip().upper()
        s = self.__find(sid)
        if not s:
            print("  ❌ Student not found.")
            return
        subject = input("  Subject    : ").strip()
        try:
            score = float(input("  Score(0-100): "))
            s.add_grade(subject, score)
            self.__save()
        except ValueError as e:
            print(f"  ❌ {e}")

    def search(self):
        print("\n── 🔍 Search ─────────────────────────")
        keyword = input("  Search (name/course): ").strip().lower()
        results = [s for s in self.__students
                   if keyword in s.name.lower() or keyword in s.course.lower()]
        if not results:
            print("  No results found.")
        for s in results:
            print(f"  {s}")

    def delete_student(self):
        sid = input("\n  Enter Student ID to delete: ").strip().upper()
        s = self.__find(sid)
        if not s:
            print("  ❌ Student not found.")
            return
        confirm = input(f"  Delete '{s.name}'? (yes/no): ").lower()
        if confirm == "yes":
            self.__students.remove(s)
            self.__save()
            print("  ✅ Student deleted.")

    def statistics(self):
        print("\n── 📊 Statistics ─────────────────────")
        if not self.__students:
            print("  No data.")
            return
        avgs = [s.average() for s in self.__students]
        print(f"  Total Students : {len(self.__students)}")
        print(f"  Highest Avg    : {max(avgs):.1f}")
        print(f"  Lowest Avg     : {min(avgs):.1f}")
        print(f"  Class Average  : {sum(avgs)/len(avgs):.1f}")
        pass_count = sum(1 for s in self.__students if s.average() >= 50)
        print(f"  Passing        : {pass_count}/{len(self.__students)}")
        # Top students
        top = sorted(self.__students, key=lambda s: s.average(), reverse=True)[:3]
        print("  Top 3 Students:")
        for i, s in enumerate(top, 1):
            print(f"    {i}. {s.name:<20} {s.average():.1f} ({s.letter_grade()})")

    def run(self):
        print("\n" + "="*44)
        print("    🎓  STUDENT MANAGEMENT SYSTEM")
        print("="*44)
        menu = {
            "1": ("Add Student",     self.add_student),
            "2": ("View All",        self.view_all),
            "3": ("View Report Card",self.view_student),
            "4": ("Add Grade",       self.add_grade),
            "5": ("Search",          self.search),
            "6": ("Delete Student",  self.delete_student),
            "7": ("Statistics",      self.statistics),
            "0": ("Exit",            None),
        }
        while True:
            print("\n" + "─"*30)
            for k, (label, _) in menu.items():
                print(f"  [{k}] {label}")
            choice = input("  Choice: ").strip()
            if choice == "0":
                print("\n  👋 Goodbye!")
                break
            elif choice in menu:
                menu[choice][1]()
            else:
                print("  ⚠️  Invalid choice.")

if __name__ == "__main__":
    StudentManagementSystem().run()
