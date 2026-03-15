"""
Exploratory Data Analysis – Ukrainian Hourly Weather Data
=========================================================

Run:
    python3 weather_eda.py

All figures are saved to ./eda_output/
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from matplotlib.ticker import MaxNLocator

warnings.filterwarnings("ignore")

# ── Output directory ──────────────────────────────────────────────────────────
OUT = "eda_output"
os.makedirs(OUT, exist_ok=True)

# ── Global style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
})

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"✔ saved → {path}")

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════════
print("Loading data...")

CSV = "<your path for weather dataset>"
df = pd.read_csv(CSV, low_memory=False)

# Datetime parsing
df["day_datetime"] = pd.to_datetime(df["day_datetime"], errors="coerce")

df["hour_datetime"] = pd.to_datetime(
    df["day_datetime"].dt.strftime("%Y-%m-%d") + " " + df["hour_datetime"].astype(str),
    errors="coerce"
)

df["year"] = df["day_datetime"].dt.year
df["month"] = df["day_datetime"].dt.month
df["hour_of_day"] = df["hour_datetime"].dt.hour

# Season
df["season"] = df["month"].map({
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Autumn", 10: "Autumn", 11: "Autumn"
})

# ── City column automatically ─────────────────────────────────────────────────
if "city" not in df.columns:
    if "city_address" in df.columns:
        df["city"] = df["city_address"].astype(str)
    else:
        raise ValueError("Dataset must contain 'city' or 'city_address' column")

# Daily dataset
daily = df.drop_duplicates(subset=["city", "day_datetime"]).copy()

# Cities list
CITIES = sorted(df["city"].dropna().unique())

# Automatic palette
palette = sns.color_palette("tab10", n_colors=len(CITIES))
pal = dict(zip(CITIES, palette))

season_order = ["Winter", "Spring", "Summer", "Autumn"]

season_pal = {
    "Winter": "#AED6F1",
    "Spring": "#A9DFBF",
    "Summer": "#F9E79F",
    "Autumn": "#F0B27A",
}

month_names = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

print(f"Rows: {len(df)}")
print(f"Cities: {CITIES}")
print()

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 1 – Monthly mean temperature
# ═══════════════════════════════════════════════════════════════════════════════
monthly_temp = (
    daily.groupby(["city","year","month"])["day_temp"]
    .mean()
    .reset_index()
)

monthly_temp["period"] = pd.to_datetime(
    monthly_temp["year"].astype(str) + "-" +
    monthly_temp["month"].astype(str).str.zfill(2) + "-01"
)

fig, ax = plt.subplots(figsize=(14,5))

for city, grp in monthly_temp.groupby("city"):
    grp = grp.sort_values("period")
    ax.plot(grp["period"], grp["day_temp"],
            label=city, color=pal[city], marker="o")

ax.axhline(0, ls="--", color="gray")
ax.legend()
ax.set_title("Monthly Mean Temperature by City")
ax.set_ylabel("Temperature °C")

save(fig, "fig01_monthly_temp_by_city.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 2 – Temperature violin
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12,6))

sns.violinplot(
    data=df.dropna(subset=["hour_temp"]),
    x="city",
    y="hour_temp",
    order=CITIES,
    palette=[pal[c] for c in CITIES],
    inner="quartile",
    ax=ax
)

ax.axhline(0, ls="--")
ax.set_title("Hourly Temperature Distribution")

save(fig, "fig02_temp_violin.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 3 – Seasonal temperature boxplot
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13,6))

sns.boxplot(
    data=df.dropna(subset=["hour_temp"]),
    x="season",
    y="hour_temp",
    hue="city",
    order=season_order,
    palette=pal,
    ax=ax
)

ax.axhline(0, ls="--")
ax.set_title("Seasonal Temperature by City")

save(fig, "fig03_seasonal_temp_boxplot.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 4 – Diurnal temperature
# ═══════════════════════════════════════════════════════════════════════════════
diurnal = (
    df.groupby(["season","hour_of_day"])["hour_temp"]
    .agg(["mean","std"])
    .reset_index()
)

fig, axes = plt.subplots(2,2,figsize=(12,8),sharex=True,sharey=True)

for ax, season in zip(axes.flat, season_order):

    sub = diurnal[diurnal["season"]==season]

    ax.plot(sub["hour_of_day"], sub["mean"], color=season_pal[season])

    ax.fill_between(
        sub["hour_of_day"],
        sub["mean"]-sub["std"],
        sub["mean"]+sub["std"],
        alpha=0.3,
        color=season_pal[season]
    )

    ax.set_title(season)

save(fig,"fig04_diurnal_temp_profile.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 5 – Temperature anomaly
# ═══════════════════════════════════════════════════════════════════════════════
lt_mean = daily.groupby(["city","month"])["day_temp"].mean()

monthly = daily.groupby(["city","year","month"])["day_temp"].mean().reset_index()

monthly = monthly.join(lt_mean, on=["city","month"], rsuffix="_lt")

monthly["anomaly"] = monthly["day_temp"] - monthly["day_temp_lt"]

monthly["period"] = pd.to_datetime(
    monthly["year"].astype(str)+"-"+monthly["month"].astype(str).str.zfill(2)+"-01"
)

fig, ax = plt.subplots(figsize=(14,6))

for city, grp in monthly.groupby("city"):
    ax.plot(grp["period"], grp["anomaly"], label=city)

ax.axhline(0,color="black")
ax.legend()

save(fig,"fig05_temp_anomaly.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 6 – Precipitation heatmap
# ═══════════════════════════════════════════════════════════════════════════════
precip = (
    daily.groupby(["city","month"])["day_precip"]
    .mean()
    .reset_index()
    .pivot(index="city",columns="month",values="day_precip")
)

precip.columns = month_names

fig, ax = plt.subplots(figsize=(12,5))

sns.heatmap(
    precip.fillna(0),
    cmap="Blues",
    annot=True,
    fmt=".1f",
    ax=ax
)

save(fig,"fig06_precipitation_heatmap.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 7 – Annual precipitation
# ═══════════════════════════════════════════════════════════════════════════════
ann = daily.groupby(["city","year"])["day_precip"].sum().reset_index()

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=ann,
    x="year",
    y="day_precip",
    hue="city",
    palette=pal,
    ax=ax
)

save(fig,"fig07_annual_precipitation.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 8 – Snow depth
# ═══════════════════════════════════════════════════════════════════════════════
snow = (
    daily.groupby(["city","month"])["day_snowdepth"]
    .max()
    .reset_index()
    .pivot(index="city",columns="month",values="day_snowdepth")
)

snow.columns = month_names

fig, ax = plt.subplots(figsize=(12,5))

sns.heatmap(
    snow.fillna(0),
    cmap="Blues",
    annot=True,
    fmt=".1f",
    ax=ax
)

save(fig,"fig08_snowdepth_heatmap.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 9 – Wind speed KDE
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10,5))

for city in CITIES:
    df[df["city"]==city]["hour_windspeed"].dropna().plot.kde(
        ax=ax,
        label=city
    )

ax.legend()
ax.set_xlim(left=0)

save(fig,"fig09_wind_speed_kde.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 10 – Wind rose
# ═══════════════════════════════════════════════════════════════════════════════
wind_df = df[["hour_winddir","hour_windspeed"]].dropna()

labels_dir = ["N","NE","E","SE","S","SW","W","NW"]

wind_df["dir_bin"] = pd.cut(
    (wind_df["hour_winddir"]+22.5)%360,
    bins=np.arange(0,405,45),
    labels=labels_dir
)

speed_bins = [0,10,20,30,np.inf]
speed_labels = ["0–10","10–20","20–30",">30"]

wind_df["speed_cat"] = pd.cut(
    wind_df["hour_windspeed"],
    bins=speed_bins,
    labels=speed_labels
)

rose = wind_df.groupby(["dir_bin","speed_cat"]).size().unstack(fill_value=0)

angles = np.linspace(0,2*np.pi,len(labels_dir),endpoint=False)

fig, ax = plt.subplots(subplot_kw={"projection":"polar"},figsize=(8,8))

bottom = np.zeros(len(labels_dir))

for sp in speed_labels:

    vals = rose.get(sp,pd.Series(0,index=labels_dir)).values

    ax.bar(
        angles,
        vals,
        bottom=bottom
    )

    bottom += vals

ax.set_xticks(angles)
ax.set_xticklabels(labels_dir)

save(fig,"fig10_wind_rose.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 11 – Humidity vs temp
# ═══════════════════════════════════════════════════════════════════════════════
valid = df[["hour_temp","hour_humidity"]].dropna()

fig, ax = plt.subplots(figsize=(8,6))

hb = ax.hexbin(
    valid["hour_temp"],
    valid["hour_humidity"],
    gridsize=60
)

fig.colorbar(hb, ax=ax)

save(fig,"fig11_humidity_vs_temp_hexbin.png")

# ═══════════════════════════════════════════════════════════════════════════════
# FIG 12 – Correlation
# ═══════════════════════════════════════════════════════════════════════════════
hour_cols = [
"hour_temp","hour_feelslike","hour_humidity","hour_dew",
"hour_precip","hour_windspeed","hour_windgust",
"hour_pressure","hour_visibility","hour_cloudcover",
"hour_solarradiation","hour_uvindex"
]

corr = df[hour_cols].corr()

fig, ax = plt.subplots(figsize=(10,8))

sns.heatmap(
    corr,
    cmap="RdBu_r",
    center=0,
    annot=True,
    fmt=".2f",
    ax=ax
)

save(fig,"fig12_correlation_heatmap.png")

print("EDA finished.")