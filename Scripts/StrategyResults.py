import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 🔧 Change this to your CSV file path
file_path = '/Users/zuhairsaeed/Downloads/33.csv'
df = pd.read_csv(file_path)

# === Clean
df['Roomsbooked'] = pd.to_numeric(df['Roomsbooked'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df.dropna(inplace=True)

# === Zero-booking flag
df['ZeroBookings'] = df['RoomsBooked'] == 0

# === 📊 Revenue by Weather
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Weather", y="Revenue", estimator='mean', ci=None, palette="pastel")
plt.title(" Average Revenue by Weather")
plt.ylabel("Avg Revenue")
plt.tight_layout()
plt.show()

# === 📊 Revenue by Day of Week
plt.figure(figsize=(10, 5))
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.barplot(data=df, x="DayOfWeek", y="Revenue", estimator='mean', ci=None, order=order, palette="muted")
plt.title(" Average Revenue by Day of Week")
plt.ylabel("Avg Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === 🔥 Heatmap: Weather vs DayOfWeek
pivot = df.pivot_table(values='Revenue', index='Weather', columns='DayOfWeek', aggfunc='mean')
plt.figure(figsize=(10, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Revenue Heatmap: Weather × Day of Week")
plt.tight_layout()
plt.show()

# === 📉 Rainy Day Price vs Bookings
rainy_df = df[df['Weather'] == 'Rainy']
if not rainy_df.empty:
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=rainy_df, x='Price', y='RoomsBooked', marker="o", label="Rainy Days")
    plt.title("🌧️ Price vs Bookings (Rainy Days)")
    plt.xlabel("Price")
    plt.ylabel("Rooms Booked")
    plt.tight_layout()
    plt.show()

# === ❌ Zero-Booking Days Map
if df['ZeroBookings'].any():
    zero = df[df['ZeroBookings']]
    plt.figure(figsize=(10, 4))
    sns.scatterplot(data=zero, x='Day', y='Revenue', hue='Weather', style='DayOfWeek', s=100)
    plt.title("❌ Zero-Booking Days")
    plt.xlabel("Day")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()
