"""
Exploratory Data Analysis – Ukrainian Air Raid Alarms
=====================================================


Run:
    python3 alarms_eda.py

Output:
    ./eda_output/ figures
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

DATA_FILE = "<your path for alarms dataset>"
OUT = "alarms_eda_output"
os.makedirs(OUT, exist_ok=True)

def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, name))
    plt.close()
    print("Saved:", name)

# ─────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────

df = pd.read_csv(DATA_FILE, sep=";")

df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

df["duration_min"] = (df["end"] - df["start"]).dt.total_seconds() / 60

df["date"] = df["start"].dt.date
df["year"] = df["start"].dt.year
df["month"] = df["start"].dt.month
df["hour"] = df["start"].dt.hour

# ─────────────────────────────────────
# 1 Alarms by region
# ─────────────────────────────────────

plt.figure(figsize=(12,8))

order = df["region_city"].value_counts().index

sns.countplot(
    data=df,
    y="region_city",
    order=order
)

plt.title("Number of Air Raid Alarms by Ukrainian Region")
plt.xlabel("Number of Alarms")
plt.ylabel("Region")

save("01_alarms_by_region.png")

# ─────────────────────────────────────
# 2 Alarm duration distribution
# ─────────────────────────────────────

plt.figure(figsize=(10,5))

sns.histplot(df["duration_min"], bins=50)

plt.title("Distribution of Air Raid Alarm Duration")
plt.xlabel("Alarm Duration (minutes)")
plt.ylabel("Frequency")

save("02_duration_distribution.png")

# ─────────────────────────────────────
# 3 Daily alarms over time
# ─────────────────────────────────────

daily = df.groupby("date").size()

plt.figure(figsize=(14,5))

daily.plot()

plt.title("Number of Air Raid Alarms per Day")
plt.xlabel("Date")
plt.ylabel("Number of Alarms")

save("03_daily_alarms.png")

# ─────────────────────────────────────
# 4 Monthly alarm trend
# ─────────────────────────────────────

monthly = df.groupby(["year","month"]).size()

plt.figure(figsize=(12,5))

monthly.plot(marker="o")

plt.title("Monthly Number of Air Raid Alarms")
plt.xlabel("Year-Month")
plt.ylabel("Number of Alarms")

save("04_monthly_alarms.png")

# ─────────────────────────────────────
# 5 Alarms by hour of day
# ─────────────────────────────────────

plt.figure(figsize=(10,5))

sns.countplot(data=df, x="hour")

plt.title("Air Raid Alarm Frequency by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Alarms")

save("05_alarms_by_hour.png")

# ─────────────────────────────────────
# 6 Alarm duration by region
# ─────────────────────────────────────

top_regions = df["region_city"].value_counts().head(10).index

plt.figure(figsize=(12,6))

sns.boxplot(
    data=df[df["region_city"].isin(top_regions)],
    x="region_city",
    y="duration_min"
)

plt.title("Alarm Duration Distribution in Top 10 Regions")
plt.xlabel("Region")
plt.ylabel("Duration (minutes)")
plt.xticks(rotation=45)

save("06_duration_by_region.png")

# ─────────────────────────────────────
# 7 Average alarm duration per region
# ─────────────────────────────────────

avg_duration = df.groupby("region_city")["duration_min"].mean().sort_values()

plt.figure(figsize=(12,8))

avg_duration.plot(kind="barh")

plt.title("Average Air Raid Alarm Duration by Region")
plt.xlabel("Average Duration (minutes)")
plt.ylabel("Region")

save("07_avg_duration_region.png")

# ─────────────────────────────────────
# 8 Heatmap of alarms by region and month
# ─────────────────────────────────────

heat = df.groupby(["region_city","month"]).size().unstack(fill_value=0)

plt.figure(figsize=(12,8))

sns.heatmap(heat, cmap="Reds")

plt.title("Air Raid Alarm Frequency by Region and Month")
plt.xlabel("Month")
plt.ylabel("Region")

save("08_region_month_heatmap.png")

# ─────────────────────────────────────
# 9 Alarm duration vs start hour
# ─────────────────────────────────────

plt.figure(figsize=(10,6))

sns.scatterplot(
    data=df.sample(3000),
    x="hour",
    y="duration_min",
    alpha=0.5
)

plt.title("Relationship Between Alarm Start Hour and Duration")
plt.xlabel("Hour of Day")
plt.ylabel("Duration (minutes)")

save("09_hour_vs_duration.png")

# ─────────────────────────────────────
# 10 Distribution of alarms by weekday
# ─────────────────────────────────────

df["weekday"] = df["start"].dt.day_name()

plt.figure(figsize=(10,5))

sns.countplot(
    data=df,
    x="weekday",
    order=[
        "Monday","Tuesday","Wednesday",
        "Thursday","Friday","Saturday","Sunday"
    ]
)

plt.title("Air Raid Alarms by Day of Week")
plt.xlabel("Weekday")
plt.ylabel("Number of Alarms")

save("10_weekday_distribution.png")

# ─────────────────────────────────────
# 11 Duration vs month
# ─────────────────────────────────────

plt.figure(figsize=(10,5))

sns.boxplot(
    data=df,
    x="month",
    y="duration_min"
)

plt.title("Air Raid Alarm Duration by Month")
plt.xlabel("Month")
plt.ylabel("Duration (minutes)")

save("11_duration_by_month.png")

# ─────────────────────────────────────
# 12 Longest alarms
# ─────────────────────────────────────

top = df.sort_values("duration_min", ascending=False).head(20)

plt.figure(figsize=(10,6))

sns.barplot(
    data=top,
    x="duration_min",
    y="region_city"
)

plt.title("Top 20 Longest Air Raid Alarms")
plt.xlabel("Duration (minutes)")
plt.ylabel("Region")

save("12_longest_alarms.png")

print("\nEDA completed. Figures saved in:", OUT)