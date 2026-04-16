# 📊 Student & Sales Data Analyzer — Data Science Project

> **Project** | Data analysis with Pandas, NumPy, Matplotlib & Seaborn

A complete data science project that analyzes **student performance** and **sales data** —
generating rich visualizations and a summary report automatically.

---

## 🔍 What It Analyzes

### 📚 Student Performance
- Grade distribution (A+ to F)
- Subject-wise average scores
- Pass/fail rate
- Score distribution histogram
- Subject correlations (heatmap)
- Average score by course & gender
- Attendance vs performance scatter plot

### 💼 Sales Data
- Total revenue by product and region
- Monthly revenue trend line
- Discount vs revenue relationship
- Regional market share (pie chart)
- Top and bottom performers

---

## 📁 Project Structure

```
datascience/
├── generate_data.py        ← Step 1: Creates sample CSV datasets
├── analysis.py             ← Step 2: Full analysis + charts
├── requirements.txt        ← pandas, numpy, matplotlib, seaborn
├── data/
│   ├── students.csv        ← 30 students, 5 subjects (auto-generated)
│   └── sales.csv           ← 500 sales records (auto-generated)
└── reports/                ← Auto-created by analysis.py
    ├── student_dashboard.png
    ├── sales_dashboard.png
    └── summary_report.txt
```

---

## 🚀 How to Run

```bash
# 1. Navigate to project folder
cd datascience

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample data
python generate_data.py

# 5. Run full analysis
python analysis.py

# 6. View results in reports/ folder
```

---

## 📊 Output Charts

### Student Dashboard (`reports/student_dashboard.png`)
- Bar chart — Grade distribution
- Horizontal bar — Avg score per subject
- Histogram — Score distribution with mean line
- Heatmap — Subject correlations
- Horizontal bar — Avg score by course
- Scatter — Attendance vs Score (by gender, with trend line)

### Sales Dashboard (`reports/sales_dashboard.png`)
- Horizontal bar — Revenue by product
- Pie chart — Revenue by region
- Line chart — Monthly revenue trend
- Scatter — Discount % vs Revenue by region

---

## 🧠 Techniques Used

| Technique | Library |
|-----------|---------|
| Data loading & cleaning | `pandas` |
| Descriptive statistics | `pandas`, `numpy` |
| Derived columns & groupby | `pandas` |
| Correlation analysis | `pandas.DataFrame.corr()` |
| Bar, pie, scatter, line charts | `matplotlib` |
| Statistical heatmap | `seaborn` |
| Grid layouts | `matplotlib.gridspec` |
| Trend line fitting | `numpy.polyfit` |

---

## 🛠️ Tech Stack

- **Python 3.7+**
- **pandas** — data loading, wrangling, groupby, statistics
- **numpy** — numerical operations, trend fitting
- **matplotlib** — all chart rendering
- **seaborn** — heatmaps, themed styling

---

## 📋 Sample Output

```
==============================
  DATA ANALYSIS REPORT
  Generated: 2024-06-15 14:30
==============================

STUDENT PERFORMANCE
  Total Students : 30
  Pass Rate      : 86.7%
  Class Average  : 72.45
  Top Student    : Carol (91.2)
  Best Subject   : Computer (76.3)

SALES SUMMARY
  Total Revenue  : ₹12,847,320
  Best Product   : Laptop (₹3,241,500)
  Best Region    : North (₹3,456,780)
  Total Quantity : 5,423 units
```

---

### Developed by Bishwashree Chakraborty