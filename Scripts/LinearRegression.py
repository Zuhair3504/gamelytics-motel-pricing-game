import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import warnings
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Add polynomial term for PriceSet
from sklearn.pipeline import make_pipeline


warnings.filterwarnings("ignore")

# === Load & Clean Data ===
df = pd.read_csv("Your Data Folder Directory")
df = df.rename(columns={'Day': 'DayOfMonth', 'Price': 'PriceSet'})
df['DayOfMonth'] = pd.to_numeric(df['DayOfMonth'], errors='coerce')
df['RoomsBooked'] = pd.to_numeric(df['RoomsBooked'], errors='coerce')
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df.dropna(inplace=True)


# Features and target for volume model
features = ['Weather', 'DayOfWeek', 'DayOfMonth', 'PriceSet']

# === Preprocessing: one-hot for categorical ===
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first'), ['Weather', 'DayOfWeek'])
], remainder='passthrough')

# === Volume Model: Linear Regression for RoomsBooked ===
volume_model = Pipeline([
    ('pre', preprocessor),
    ('reg', LinearRegression())
])
volume_model.fit(df[features], df['RoomsBooked'])

# === Revenue Per Room Model ===
df['RevPerRoom'] = df['Revenue'] / df['RoomsBooked']
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['RevPerRoom'])

revpar_model = Pipeline([
    ('pre', preprocessor),
    ('reg', LinearRegression())
])
revpar_model.fit(df[features], df['RevPerRoom'])

print(" Linear Regression models trained (volume + RevPAR).")

# --- Polynomial Features for Price ---
poly_features = ColumnTransformer([
    ('price_poly', PolynomialFeatures(degree=2, include_bias=False), ['PriceSet']),
    ('cat', OneHotEncoder(drop='first'), ['Weather', 'DayOfWeek']),
], remainder='passthrough')

# --- Fit volume model with polynomial features ---
volume_model = Pipeline([
    ('pre', poly_features),
    ('reg', LinearRegression())
])
volume_model.fit(df[features], df['RoomsBooked'])  # ✅ fit globally

# === Smart Pricing Strategy ===
def get_best_price (weather, day_of_week, day_of_month, price_range=None):
    if price_range is None:
        price_range = np.arange(50, 121, 5)

    # Clamp range
    price_range = price_range[(price_range >= 50) & (price_range <= 120)]

    # Known capped days
    capped_days = {7, 10, 14, 15, 20, 21, 26}

    test_df = pd.DataFrame({
        'Weather': [weather] * len(price_range),
        'DayOfWeek': [day_of_week] * len(price_range),
        'DayOfMonth': [day_of_month] * len(price_range),
        'PriceSet': price_range
    })
    
    

    if day_of_month in capped_days:
        predicted_revpar = revpar_model.predict(test_df)
        best_idx = np.argmax(predicted_revpar)
        strategy = "RevPAR"
        best_metric = predicted_revpar[best_idx]
    else:
        predicted_bookings = volume_model.predict(test_df)
        best_idx = np.argmax(predicted_bookings)
        strategy = "Volume"
        best_metric = predicted_bookings[best_idx]

    get_best_price = price_range[best_idx]

    print(f"📅 Day {day_of_month} | Strategy: {strategy} | Price: ${int(get_best_price)} | Predicted: {round(best_metric, 2)}")

    return int(get_best_price), int(best_metric), round(best_metric, 2)  # 👈 safe unpacking

