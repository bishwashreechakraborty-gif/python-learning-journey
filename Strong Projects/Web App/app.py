# ============================================================
#  Web App Project: Personal Expense Tracker
#  Stack : Flask (Python), SQLite, HTML/CSS/JS
#  Run   : pip install flask && python app.py
#  Open  : http://127.0.0.1:5000
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "expense_tracker_secret_key_2024"

DB_PATH = "expenses.db"


# ────────────────────────────────────────────────────────────
#  DATABASE SETUP
# ────────────────────────────────────────────────────────────

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row      # access columns by name
    return conn

def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                amount      REAL    NOT NULL,
                category    TEXT    NOT NULL,
                date        TEXT    NOT NULL,
                note        TEXT    DEFAULT '',
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS budgets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                category    TEXT    NOT NULL UNIQUE,
                monthly_limit REAL  NOT NULL
            );
        """)
        # Seed some sample data if empty
        count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        if count == 0:
            today = datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            sample_data = [
                ("Groceries",       450.0, "Food",          yesterday, "Weekly shopping"),
                ("Netflix",         649.0, "Entertainment", yesterday, "Monthly subscription"),
                ("Electricity Bill",1200.0,"Bills",         today,     "June bill"),
                ("Lunch",           180.0, "Food",          today,     "Canteen"),
                ("Bus Pass",        500.0, "Transport",     today,     "Monthly pass"),
                ("Books",           350.0, "Education",     today,     "Python book"),
            ]
            conn.executemany(
                "INSERT INTO expenses (title, amount, category, date, note) VALUES (?,?,?,?,?)",
                sample_data
            )
        print("  ✅ Database initialized.")

CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Education",
               "Shopping", "Health", "Savings", "Other"]


# ────────────────────────────────────────────────────────────
#  ROUTES
# ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Dashboard: show summary + recent expenses."""
    conn = get_db()

    # Recent expenses
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY date DESC, id DESC LIMIT 10"
    ).fetchall()

    # Total by category (this month)
    month = datetime.now().strftime("%Y-%m")
    by_category = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE date LIKE ?
        GROUP BY category
        ORDER BY total DESC
    """, (f"{month}%",)).fetchall()

    # Monthly totals (last 6 months)
    monthly = conn.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    """).fetchall()

    # Grand total this month
    month_total = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?",
        (f"{month}%",)
    ).fetchone()[0]

    # Grand total all time
    all_total = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    ).fetchone()[0]

    conn.close()
    return render_template("index.html",
        expenses=expenses,
        by_category=by_category,
        monthly=monthly,
        month_total=month_total,
        all_total=all_total,
        current_month=datetime.now().strftime("%B %Y"),
        categories=CATEGORIES,
    )


@app.route("/expenses")
def list_expenses():
    """List all expenses with search & filter."""
    conn = get_db()
    category = request.args.get("category", "")
    search   = request.args.get("search", "")
    date_from= request.args.get("date_from", "")
    date_to  = request.args.get("date_to", "")

    query  = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"; params.append(category)
    if search:
        query += " AND (title LIKE ? OR note LIKE ?)"; params += [f"%{search}%", f"%{search}%"]
    if date_from:
        query += " AND date >= ?"; params.append(date_from)
    if date_to:
        query += " AND date <= ?"; params.append(date_to)

    query += " ORDER BY date DESC, id DESC"
    expenses = conn.execute(query, params).fetchall()
    total = sum(e["amount"] for e in expenses)
    conn.close()

    return render_template("expenses.html",
        expenses=expenses, total=total,
        categories=CATEGORIES,
        filters={"category": category, "search": search,
                 "date_from": date_from, "date_to": date_to},
    )


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    """Add a new expense."""
    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        amount   = request.form.get("amount", "")
        category = request.form.get("category", "")
        date     = request.form.get("date", "")
        note     = request.form.get("note", "").strip()

        # Validation
        errors = []
        if not title:          errors.append("Title is required.")
        if not amount:         errors.append("Amount is required.")
        if not category:       errors.append("Category is required.")
        if not date:           errors.append("Date is required.")
        try:
            amount = float(amount)
            if amount <= 0: errors.append("Amount must be positive.")
        except ValueError:
            errors.append("Amount must be a valid number.")

        if errors:
            for e in errors: flash(e, "error")
            return render_template("add.html", categories=CATEGORIES,
                                   today=datetime.now().strftime("%Y-%m-%d"))

        with get_db() as conn:
            conn.execute(
                "INSERT INTO expenses (title, amount, category, date, note) VALUES (?,?,?,?,?)",
                (title, amount, category, date, note)
            )
        flash(f"✅ Expense '{title}' (₹{amount:.2f}) added!", "success")
        return redirect(url_for("index"))

    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("add.html", categories=CATEGORIES, today=today)


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    """Edit an existing expense."""
    conn = get_db()
    expense = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if not expense:
        flash("Expense not found.", "error")
        return redirect(url_for("list_expenses"))

    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        amount   = float(request.form.get("amount", 0))
        category = request.form.get("category", "")
        date     = request.form.get("date", "")
        note     = request.form.get("note", "").strip()

        conn.execute(
            "UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=?",
            (title, amount, category, date, note, expense_id)
        )
        conn.commit()
        conn.close()
        flash("✅ Expense updated!", "success")
        return redirect(url_for("list_expenses"))

    conn.close()
    return render_template("edit.html", expense=expense, categories=CATEGORIES)


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    """Delete an expense."""
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    flash("🗑️ Expense deleted.", "info")
    return redirect(url_for("list_expenses"))


@app.route("/api/summary")
def api_summary():
    """JSON API endpoint — useful for JS charts."""
    conn = get_db()
    month = datetime.now().strftime("%Y-%m")
    by_cat = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses WHERE date LIKE ?
        GROUP BY category ORDER BY total DESC
    """, (f"{month}%",)).fetchall()

    monthly = conn.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses GROUP BY month ORDER BY month DESC LIMIT 6
    """).fetchall()
    conn.close()

    return jsonify({
        "by_category": [{"category": r["category"], "total": r["total"]} for r in by_cat],
        "monthly":     [{"month": r["month"], "total": r["total"]} for r in monthly],
    })


# ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("\n  🚀 Expense Tracker running!")
    print("  Open: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
