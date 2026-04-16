# ============================================================
#  Data Science Project: Student & Sales Analyzer
#  Libraries: pandas, numpy, matplotlib, seaborn
#
#  Setup:
#    pip install pandas numpy matplotlib seaborn
#    python generate_data.py   ← create datasets first
#    python analysis.py        ← run full analysis
# ============================================================

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# ── Check dependencies ────────────────────────────────────
missing = []
for lib in ["pandas", "numpy", "matplotlib", "seaborn"]:
    try: __import__(lib)
    except ImportError: missing.append(lib)

if missing:
    print(f"❌ Missing libraries: {', '.join(missing)}")
    print(f"   Run: pip install {' '.join(missing)}")
    sys.exit(1)

# ── Style ─────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams.update({"figure.dpi": 100, "font.size": 10})

os.makedirs("reports", exist_ok=True)

print("=" * 60)
print("  📊 DATA SCIENCE PROJECT — Student & Sales Analyzer")
print("=" * 60)


# ════════════════════════════════════════════════════════════
#  PART A: STUDENT PERFORMANCE ANALYSIS
# ════════════════════════════════════════════════════════════

print("\n" + "─" * 60)
print("  PART A: STUDENT PERFORMANCE ANALYSIS")
print("─" * 60)

# Load data
df = pd.read_csv("data/students.csv")
subjects = ["math", "science", "english", "history", "computer"]

# ── A1. Dataset Overview ──────────────────────────────────
print("\n📋 Dataset Overview:")
print(f"  Shape      : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Columns    : {list(df.columns)}")
print(f"\n  First 3 rows:\n{df.head(3).to_string(index=False)}")

print(f"\n📊 Missing values:\n{df.isnull().sum()}")
print(f"\n📊 Data types:\n{df.dtypes}")


# ── A2. Compute derived columns ───────────────────────────
df["total"]   = df[subjects].sum(axis=1)
df["average"] = df[subjects].mean(axis=1).round(2)
df["grade"]   = df["average"].apply(lambda x:
    "A+" if x >= 90 else "A" if x >= 80 else "B" if x >= 70 else
    "C" if x >= 60 else "D" if x >= 50 else "F"
)
df["pass"] = df["average"] >= 50

print("\n📊 Score Statistics:")
print(df[subjects + ["average"]].describe().round(2).to_string())


# ── A3. Top and Bottom students ───────────────────────────
print("\n🏆 Top 5 Students:")
top5 = df.nlargest(5, "average")[["name", "course", "average", "grade"]]
print(top5.to_string(index=False))

print("\n⚠️  Bottom 5 Students:")
bot5 = df.nsmallest(5, "average")[["name", "course", "average", "grade"]]
print(bot5.to_string(index=False))


# ── A4. Grade distribution ────────────────────────────────
grade_dist = df["grade"].value_counts().sort_index()
pass_rate = df["pass"].mean() * 100
print(f"\n📊 Grade Distribution:\n{grade_dist.to_string()}")
print(f"\n  Pass Rate: {pass_rate:.1f}%")


# ── A5. Average by course ──────────────────────────────────
course_avg = df.groupby("course")["average"].agg(["mean","std","count"])
course_avg.columns = ["Mean", "Std", "Count"]
print(f"\n📊 Average Score by Course:\n{course_avg.round(2).to_string()}")


# ── A6. Gender analysis ───────────────────────────────────
gender_avg = df.groupby("gender")["average"].mean().round(2)
print(f"\n📊 Average Score by Gender:\n{gender_avg.to_string()}")


# ── A7. Correlation matrix ────────────────────────────────
corr = df[subjects].corr()
print(f"\n📊 Subject Correlations (top 3):")
pairs = [(corr.loc[a,b], a, b)
         for i,a in enumerate(subjects)
         for j,b in enumerate(subjects) if j > i]
for val, a, b in sorted(pairs, reverse=True)[:3]:
    print(f"  {a} ↔ {b}: {val:.3f}")


# ── A8. Attendance impact ──────────────────────────────────
df["att_group"] = pd.cut(df["attendance"],
                         bins=[0, 70, 80, 90, 101],
                         labels=["<70%", "70–80%", "80–90%", ">90%"])
att_analysis = df.groupby("att_group", observed=True)["average"].mean().round(2)
print(f"\n📊 Average Score by Attendance:\n{att_analysis.to_string()}")


# ── A9. Visualizations ────────────────────────────────────
print("\n🎨 Generating student visualizations...")

fig = plt.figure(figsize=(16, 12))
fig.suptitle("Student Performance Dashboard", fontsize=16, fontweight="bold", y=0.98)
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# 1. Grade distribution bar
ax1 = fig.add_subplot(gs[0, 0])
grade_order = ["A+", "A", "B", "C", "D", "F"]
grade_counts = [grade_dist.get(g, 0) for g in grade_order]
colors = ["#1a9641","#a6d96a","#ffffbf","#fdae61","#d7191c","#7b0000"]
bars = ax1.bar(grade_order, grade_counts, color=colors, edgecolor="white", linewidth=1.5)
ax1.set_title("Grade Distribution", fontweight="bold")
ax1.set_xlabel("Grade"); ax1.set_ylabel("Students")
for bar, val in zip(bars, grade_counts):
    if val: ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
                     str(val), ha="center", fontweight="bold", fontsize=9)

# 2. Average score by subject
ax2 = fig.add_subplot(gs[0, 1])
subject_means = df[subjects].mean().sort_values(ascending=False)
bars2 = ax2.barh(subject_means.index, subject_means.values, color=sns.color_palette("husl", 5))
ax2.set_title("Avg Score by Subject", fontweight="bold")
ax2.set_xlabel("Average Score")
for bar, val in zip(bars2, subject_means.values):
    ax2.text(val+0.5, bar.get_y()+bar.get_height()/2,
             f"{val:.1f}", va="center", fontsize=9)

# 3. Score distribution (histogram)
ax3 = fig.add_subplot(gs[0, 2])
ax3.hist(df["average"], bins=15, color="#4f46e5", edgecolor="white", alpha=0.85)
ax3.axvline(df["average"].mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: {df['average'].mean():.1f}")
ax3.set_title("Score Distribution", fontweight="bold")
ax3.set_xlabel("Average Score"); ax3.set_ylabel("Count")
ax3.legend(fontsize=8)

# 4. Correlation heatmap
ax4 = fig.add_subplot(gs[1, 0])
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
            ax=ax4, linewidths=0.5, annot_kws={"size": 8}, vmin=0, vmax=1)
ax4.set_title("Subject Correlations", fontweight="bold")
ax4.tick_params(axis="x", rotation=45, labelsize=8)
ax4.tick_params(axis="y", rotation=0, labelsize=8)

# 5. Average by course
ax5 = fig.add_subplot(gs[1, 1])
course_sorted = df.groupby("course")["average"].mean().sort_values()
ax5.barh(course_sorted.index, course_sorted.values,
         color=sns.color_palette("pastel", len(course_sorted)))
ax5.set_title("Avg Score by Course", fontweight="bold")
ax5.set_xlabel("Average Score")
ax5.axvline(60, color="red", linestyle="--", alpha=0.7, linewidth=1.2)

# 6. Attendance vs Score scatter
ax6 = fig.add_subplot(gs[1, 2])
colors_g = {"Male": "#3b82f6", "Female": "#ec4899"}
for gender, grp in df.groupby("gender"):
    ax6.scatter(grp["attendance"], grp["average"],
                label=gender, alpha=0.7, s=40, color=colors_g[gender])
z = np.polyfit(df["attendance"], df["average"], 1)
p = np.poly1d(z)
x_line = np.linspace(df["attendance"].min(), df["attendance"].max(), 100)
ax6.plot(x_line, p(x_line), "r--", linewidth=1.5, label="Trend")
ax6.set_title("Attendance vs Score", fontweight="bold")
ax6.set_xlabel("Attendance %"); ax6.set_ylabel("Average Score")
ax6.legend(fontsize=8)

plt.savefig("reports/student_dashboard.png", dpi=120, bbox_inches="tight")
plt.close()
print("  ✅ Saved: reports/student_dashboard.png")


# ════════════════════════════════════════════════════════════
#  PART B: SALES ANALYSIS
# ════════════════════════════════════════════════════════════

print("\n" + "─" * 60)
print("  PART B: SALES ANALYSIS")
print("─" * 60)

sales = pd.read_csv("data/sales.csv")
sales["date"] = pd.to_datetime(sales["date"])
sales["month"] = sales["date"].dt.to_period("M").astype(str)
sales["quarter"] = sales["date"].dt.quarter.apply(lambda q: f"Q{q}")

print(f"\n📋 Sales Dataset: {sales.shape[0]} records")
print(sales.head(3).to_string(index=False))

# B1. Revenue summary
total_revenue = sales["revenue"].sum()
avg_order     = sales["revenue"].mean()
print(f"\n💰 Total Revenue  : ₹{total_revenue:,.2f}")
print(f"   Average Order   : ₹{avg_order:,.2f}")
print(f"   Total Quantity  : {sales['quantity'].sum():,} units")

# B2. Revenue by product
prod_rev = sales.groupby("product")["revenue"].sum().sort_values(ascending=False)
print(f"\n📊 Revenue by Product:\n{prod_rev.apply(lambda x: f'₹{x:,.0f}').to_string()}")

# B3. Revenue by region
region_rev = sales.groupby("region")["revenue"].sum().sort_values(ascending=False)
print(f"\n📊 Revenue by Region:\n{region_rev.apply(lambda x: f'₹{x:,.0f}').to_string()}")

# B4. Monthly trend
monthly = sales.groupby("month")["revenue"].sum()
print(f"\n📊 Monthly Revenue (top 5):")
print(monthly.sort_values(ascending=False).head(5).apply(lambda x: f"₹{x:,.0f}").to_string())

# B5. Sales visualizations
print("\n🎨 Generating sales visualizations...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Sales Analysis Dashboard", fontsize=16, fontweight="bold")

# 1. Revenue by product
ax = axes[0, 0]
prod_sorted = prod_rev.sort_values()
bars = ax.barh(prod_sorted.index, prod_sorted.values / 1000,
               color=sns.color_palette("tab10", len(prod_sorted)))
ax.set_title("Revenue by Product (₹K)", fontweight="bold")
ax.set_xlabel("Revenue (₹ Thousands)")
for bar, val in zip(bars, prod_sorted.values):
    ax.text(val/1000 + 0.5, bar.get_y()+bar.get_height()/2,
            f"₹{val/1000:.1f}K", va="center", fontsize=8)

# 2. Revenue by region (pie)
ax = axes[0, 1]
wedges, texts, autotexts = ax.pie(
    region_rev.values, labels=region_rev.index,
    autopct="%1.1f%%", colors=sns.color_palette("pastel", 4),
    startangle=90, pctdistance=0.75,
)
for at in autotexts: at.set_fontsize(10)
ax.set_title("Revenue by Region", fontweight="bold")

# 3. Monthly trend line
ax = axes[1, 0]
monthly_sorted = monthly.sort_index()
ax.plot(range(len(monthly_sorted)), monthly_sorted.values / 1000,
        marker="o", linewidth=2, markersize=5, color="#4f46e5")
ax.fill_between(range(len(monthly_sorted)), monthly_sorted.values / 1000,
                alpha=0.15, color="#4f46e5")
ax.set_xticks(range(len(monthly_sorted)))
ax.set_xticklabels(monthly_sorted.index, rotation=45, fontsize=7, ha="right")
ax.set_title("Monthly Revenue Trend (₹K)", fontweight="bold")
ax.set_ylabel("Revenue (₹ Thousands)")

# 4. Discount vs Revenue scatter
ax = axes[1, 1]
for region, grp in sales.groupby("region"):
    ax.scatter(grp["discount"], grp["revenue"] / 1000,
               alpha=0.5, s=25, label=region)
ax.set_title("Discount % vs Revenue", fontweight="bold")
ax.set_xlabel("Discount (%)"); ax.set_ylabel("Revenue (₹K)")
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("reports/sales_dashboard.png", dpi=120, bbox_inches="tight")
plt.close()
print("  ✅ Saved: reports/sales_dashboard.png")


# ── Final Text Report ──────────────────────────────────────
report_lines = [
    "=" * 60,
    "  DATA ANALYSIS REPORT",
    f"  Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
    "=" * 60,
    "",
    "STUDENT PERFORMANCE",
    f"  Total Students : {len(df)}",
    f"  Pass Rate      : {pass_rate:.1f}%",
    f"  Class Average  : {df['average'].mean():.2f}",
    f"  Top Student    : {df.loc[df['average'].idxmax(), 'name']} ({df['average'].max():.1f})",
    f"  Best Subject   : {subject_means.idxmax().title()} ({subject_means.max():.1f})",
    "",
    "SALES SUMMARY",
    f"  Total Revenue  : ₹{total_revenue:,.0f}",
    f"  Best Product   : {prod_rev.idxmax()} (₹{prod_rev.max():,.0f})",
    f"  Best Region    : {region_rev.idxmax()} (₹{region_rev.max():,.0f})",
    f"  Total Quantity : {sales['quantity'].sum():,} units",
    "",
    "Charts saved to: reports/",
    "  • student_dashboard.png",
    "  • sales_dashboard.png",
]

report_text = "\n".join(report_lines)
with open("reports/summary_report.txt", "w") as f:
    f.write(report_text)

print("\n" + report_text)
print("\n✅ Analysis complete! Check the 'reports/' folder.")
