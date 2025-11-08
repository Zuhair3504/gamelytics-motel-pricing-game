import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# Load CSV
df = pd.read_csv('/Users/zuhairsaeed/Library/CloudStorage/OneDrive-Personal/SLU/Machine Learning/Motel Pricing Game/Data/merge-csv.com__67eacd10076e0.csv')

# Rename for consistency
df = df.rename(columns={'Day': 'DayOfMonth', 'Price': 'PriceSet'})

# Ensure DayOfMonth is numeric
df['DayOfMonth'] = pd.to_numeric(df['DayOfMonth'], errors='coerce')

# Feature engineering
df['IsWeekend'] = df['DayOfWeek'].isin(['Saturday', 'Sunday'])
df['MonthPeriod'] = pd.cut(df['DayOfMonth'], bins=[0, 10, 20, 31], labels=['Early', 'Mid', 'Late'])

# Optional: check for missing data
print(df.isnull().sum())


# --- Setup Plot Style ---
sns.set(style="whitegrid")

# --- 1. Price vs Rooms Booked ---
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='PriceSet', y='RoomsBooked', hue='Weather')
plt.title("Price vs Rooms Booked by Weather")
plt.savefig("price_vs_rooms_by_weather.png")
plt.clf()

# --- 2. Average Rooms Booked by Day of Week ---
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x='DayOfWeek', y='RoomsBooked', estimator='mean', ci=None)
plt.title("Average Rooms Booked by Day of Week")
plt.xticks(rotation=45)
plt.savefig("avg_rooms_by_dayofweek.png")
plt.clf()

# --- 3. Average Price by Weather ---
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Weather', y='PriceSet')
plt.title("Price Distribution by Weather")
plt.savefig("price_distribution_by_weather.png")
plt.clf()

# --- 4. Rooms Booked by Month Period ---
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='MonthPeriod', y='RoomsBooked')
plt.title("Rooms Booked by Period of Month")
plt.savefig("rooms_by_monthperiod.png")
plt.clf()

# --- 5. Weekend vs Weekday Analysis ---
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='IsWeekend', y='PriceSet')
plt.title("Price Distribution: Weekend vs Weekday")
plt.xticks([0, 1], ['Weekday', 'Weekend'])
plt.savefig("price_weekend_vs_weekday.png")
plt.clf()

plt.figure(figsize=(8, 5))
sns.barplot(data=df, x='DayOfWeek', y='Revenue', estimator='mean', ci=None, palette='coolwarm')
plt.title("Average Revenue by Day of Week")
plt.xticks(rotation=45)
plt.savefig("revenue_by_dayofweek.png")
plt.clf()

import numpy as np

# Pivot table for avg revenue by DayOfWeek and Weather
heatmap_data = df.pivot_table(values='Revenue', index='Weather', columns='DayOfWeek', aggfunc='mean')

# Create heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlOrRd")
plt.title("Average Revenue by Weather and Day of Week")
plt.savefig("revenue_heatmap_weather_dayofweek.png")
plt.clf()

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='Weather', y='Revenue', palette='Set2')
plt.title("Revenue Distribution by Weather")
plt.savefig("revenue_by_weather.png")
plt.clf()

# Already defined earlier
df['MonthPeriod'] = pd.cut(df['DayOfMonth'], bins=[0, 10, 20, 31], labels=['Early', 'Mid', 'Late'])

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='MonthPeriod', y='Revenue', palette='Blues')
plt.title("Revenue by Period of Month")
plt.savefig("revenue_by_monthperiod.png")
plt.clf()

# --- Average Rooms Booked by Day of the Month ---
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='DayOfMonth', y='RoomsBooked', estimator='mean', ci=None, marker='o')
plt.title("📅 Average Rooms Booked by Day of the Month")
plt.xlabel("Day of Month")
plt.ylabel("Avg Rooms Booked")
plt.xticks(range(1, 31))
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_rooms_by_dayofmonth.png")
plt.clf()

# --- Max Rooms Booked by Day of the Month ---
plt.figure(figsize=(10, 6))
sns.lineplot(
    data=df.groupby('DayOfMonth')['RoomsBooked'].max().reset_index(),
    x='DayOfMonth',
    y='RoomsBooked',
    marker='o',
    color='darkgreen'
)
plt.title("📈 Max Rooms Booked by Day of the Month")
plt.xlabel("Day of Month")
plt.ylabel("Max Rooms Booked")
plt.xticks(range(1, 31))
plt.grid(True)
plt.tight_layout()
plt.savefig("max_rooms_by_dayofmonth.png")
plt.clf()

# Max bookings per day
max_rooms = df.groupby('DayOfMonth')['RoomsBooked'].max().reset_index()

# Flag low-capacity days (below 90)
max_rooms['IsLimited'] = max_rooms['RoomsBooked'] < 90

# Plot
plt.figure(figsize=(10, 6))
sns.lineplot(data=max_rooms, x='DayOfMonth', y='RoomsBooked', marker='o', label='Max Rooms')
sns.scatterplot(data=max_rooms[max_rooms['IsLimited']], x='DayOfMonth', y='RoomsBooked', color='red', label='Under 90')
plt.title("🚨 Max Rooms Booked by Day (Highlighting Demand Caps)")
plt.xlabel("Day of Month")
plt.ylabel("Max Rooms Booked")
plt.xticks(range(1, 31))
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.savefig("max_rooms_highlighted.png")
plt.clf()


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/Users/zuhairsaeed/Library/CloudStorage/OneDrive-Personal/SLU/Machine Learning/Motel Pricing Game/Data/merge-csv.com__67eacd10076e0.csv')

# Clean up
df = df.rename(columns={'Day': 'DayOfMonth', 'Price': 'PriceSet'})
df['DayOfMonth'] = pd.to_numeric(df['DayOfMonth'], errors='coerce')
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df['RoomsBooked'] = pd.to_numeric(df['RoomsBooked'], errors='coerce')
df.dropna(subset=['DayOfMonth', 'DayOfWeek', 'Weather', 'Revenue', 'RoomsBooked'], inplace=True)

# Calculate RevPAR safely
df['RevPerRoom'] = df['Revenue'] / df['RoomsBooked']
df = df.replace([np.inf, -np.inf], np.nan)
df.dropna(subset=['RevPerRoom'], inplace=True)

# Group by DayOfMonth + Weather + DayOfWeek
grouped = df.groupby(['DayOfMonth', 'DayOfWeek', 'Weather'])['RevPerRoom'].mean().reset_index()

# Optional: Pivot into a grid format for visual clarity
pivot = grouped.pivot_table(index='DayOfMonth', columns=['DayOfWeek', 'Weather'], values='RevPerRoom')

# Plot heatmap
plt.figure(figsize=(18, 8))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, linecolor='gray')
plt.title("📊 Avg Revenue per Room by Day, Day of Week & Weather", fontsize=14)
plt.xlabel("Day of Week × Weather")
plt.ylabel("Day of Month")
plt.tight_layout()
plt.savefig("revpar_heatmap_day_weather_dow.png")
plt.show()


print("✅ All plots generated and saved!")
