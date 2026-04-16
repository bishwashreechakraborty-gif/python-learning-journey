# 💰 Personal Expense Tracker — Flask Web App

> **Project** | Full-stack Python web application

A complete web-based expense tracker built with **Flask + SQLite**.
Track your daily spending, filter by category, and view monthly summaries — all in your browser.

---

## 🖥️ Features

| Feature | Description |
|---------|-------------|
| ➕ Add Expense | Title, amount, category, date, optional note |
| 📋 View All | Filter by category, search by keyword, date range |
| ✏️ Edit | Update any expense in-place |
| 🗑️ Delete | Remove with confirmation prompt |
| 📊 Dashboard | Monthly totals, category breakdown, bar charts |
| 🔌 JSON API | `/api/summary` endpoint returns JSON data |
| 💾 Persistent | SQLite database — data saved between runs |
| 📱 Responsive | Works on desktop and mobile |

---

## 📁 Project Structure

```
webapp/
├── app.py                  ← Flask app (routes, DB logic)
├── requirements.txt        ← Flask==3.0.0
├── expenses.db             ← SQLite DB (auto-created on first run)
├── templates/
│   ├── base.html           ← Shared layout (navbar, alerts, footer)
│   ├── index.html          ← Dashboard with summary cards
│   ├── expenses.html       ← Full list with filters
│   ├── add.html            ← Add expense form
│   └── edit.html           ← Edit expense form
└── static/
    ├── css/style.css       ← Full responsive CSS
    └── js/charts.js        ← Auto-dismiss alerts
```

---

## 🚀 How to Run

```bash
# 1. Navigate to project folder
cd webapp

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# 5. Open in browser
http://127.0.0.1:5000
```

---

## 🗺️ Pages & Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Dashboard — summary cards + recent expenses |
| `/expenses` | GET | All expenses with search/filter |
| `/add` | GET, POST | Add new expense form |
| `/edit/<id>` | GET, POST | Edit existing expense |
| `/delete/<id>` | POST | Delete expense |
| `/api/summary` | GET | JSON: category totals + monthly trend |

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask 3.0
- **Database**: SQLite (built-in — no setup needed)
- **Frontend**: HTML5, CSS3 (custom), vanilla JavaScript
- **Templating**: Jinja2 (Flask's built-in)

---

## 📸 Screenshots

Run the app and visit `http://127.0.0.1:5000` to see:
- Dashboard with colorful summary cards and category bar charts
- Clean expense table with category color badges
- Smooth add/edit forms with validation

---

## 🔌 API Example

```bash
curl http://127.0.0.1:5000/api/summary
```

```json
{
  "by_category": [
    {"category": "Bills", "total": 1200.0},
    {"category": "Food",  "total": 630.0}
  ],
  "monthly": [
    {"month": "2024-06", "total": 3329.0}
  ]
}
```

---

### Developed by Bishwashree Chakraborty