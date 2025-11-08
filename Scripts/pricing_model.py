import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import warnings



warnings.filterwarnings("ignore")

# === Load & Clean Data ===
df = pd.read_csv('/Users/zuhairsaeed/Library/CloudStorage/OneDrive-Personal/SLU/Machine Learning/Motel Pricing Game/Data/merge-csv.com__67eacd10076e0.csv')
df = df.rename(columns={'Day': 'DayOfMonth', 'Price': 'PriceSet'})
df['DayOfMonth'] = pd.to_numeric(df['DayOfMonth'], errors='coerce')
df['RoomsBooked'] = pd.to_numeric(df['RoomsBooked'], errors='coerce')
df.dropna(inplace=True)

# Optional: Trim price range to practical levels
df = df[(df['PriceSet'] >= 50) & (df['PriceSet'] <= 110)]

# === Train on RoomsBooked ===
features = ['Weather', 'DayOfWeek', 'DayOfMonth', 'PriceSet']
target = 'RoomsBooked'

preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first'), ['Weather', 'DayOfWeek'])
], remainder='passthrough')

model = Pipeline([
    ('pre', preprocessor),
    ('reg', RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42))
])

model.fit(df[features], df[target])
print("✅ Random Forest model trained to maximize RoomsBooked.")

# === Booking-Focused Price Optimizer ===
def get_best_price(weather, day_of_week, day_of_month, price_range=None):
    if price_range is None:
        price_range = np.arange(50, 120, 5)
    # Define demand-capped days (you can update this set)
    capped_days = {7, 10, 14, 15, 20, 21, 26}

    # Build test data
    test_df = pd.DataFrame({
        'Weather': [weather] * len(price_range),
        'DayOfWeek': [day_of_week] * len(price_range),
        'DayOfMonth': [day_of_month] * len(price_range),
        'PriceSet': price_range
    })

    # Predict
    predicted_bookings = model.predict(test_df)
    predicted_revenue = predicted_bookings * price_range
    revpar = np.where(predicted_bookings > 0, predicted_revenue / predicted_bookings, 0)

    if day_of_month in capped_days:
        # 🔄 Focus on RevPAR for capped days
        best_idx = np.argmax(revpar)
        price = price_range[best_idx]
        bookings = predicted_bookings[best_idx]
        return int(price), int(bookings), round(revpar[best_idx], 2)
    else:
        # ✅ On normal days: maximize total rooms booked
        best_idx = np.argmax(predicted_bookings)
        price = price_range[best_idx]
        bookings = predicted_bookings[best_idx]
        return int(price), int(bookings), round(revpar[best_idx], 2)


