# ================================
# 1. Import Required Libraries
# ================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")


# ================================
# 2. Load & Preprocess Data
# ================================
# Load only required columns
df = pd.read_csv(
    "COMED_Data.csv",
    usecols=["Datetime", "COMED"]
)

# Remove null values
df.dropna(inplace=True)

# Convert Datetime to standardized format (day/month/year)
df["Datetime"] = pd.to_datetime(df["Datetime"], dayfirst=True)

# Sort by time
df.sort_values("Datetime", inplace=True)

# Filter data from Jan 1, 2017 onwards
df = df[df["Datetime"] >= "2017-01-01"]

# Set datetime as index
df.set_index("Datetime", inplace=True)


# ================================
# 3. High-Resolution Time Series Plot
# ================================
plt.figure(figsize=(16, 6))
plt.plot(df.index, df["COMED"], linewidth=0.6)
plt.title("COMED Energy Demand Time Series (From 2017 Onwards)")
plt.xlabel("Time")
plt.ylabel("Energy Demand (MW)")
plt.show()


# ================================
# 4. Simulate Federated Environment (10-Fold → 2 Clients)
# ================================
kf = KFold(n_splits=10, shuffle=False)

folds = []
for _, test_index in kf.split(df):
    folds.append(df.iloc[test_index])

# Combine folds into 2 clients
client_1 = pd.concat(folds[:5])
client_2 = pd.concat(folds[5:])


# ================================
# 5. Feature Engineering Function
# ================================
def create_time_features(data):
    data = data.copy()

    # Lag Features
    data["lag_1h"] = data["COMED"].shift(1)
    data["lag_24h"] = data["COMED"].shift(24)
    data["lag_168h"] = data["COMED"].shift(168)

    # Rolling Window Features
    data["rolling_24h"] = data["COMED"].rolling(24).mean()
    data["rolling_7d"] = data["COMED"].rolling(168).mean()

    # Drop NaN rows created due to lags
    data.dropna(inplace=True)

    return data


# Apply feature engineering
client_1_fe = create_time_features(client_1)
client_2_fe = create_time_features(client_2)


# ================================
# 6. Visualize Lag Relationships
# ================================
plt.figure(figsize=(14, 4))

plt.subplot(1, 3, 1)
plt.scatter(client_1_fe["lag_1h"], client_1_fe["COMED"], alpha=0.3)
plt.title("Current Load vs Previous Hour")

plt.subplot(1, 3, 2)
plt.scatter(client_1_fe["lag_24h"], client_1_fe["COMED"], alpha=0.3)
plt.title("Current Load vs Same Hour Previous Day")

plt.subplot(1, 3, 3)
plt.scatter(client_1_fe["lag_168h"], client_1_fe["COMED"], alpha=0.3)
plt.title("Current Load vs Same Hour Previous Week")

plt.tight_layout()
plt.show()


# ================================
# 7. Prepare Inputs & Targets
# ================================
FEATURES = ["lag_1h", "lag_24h", "lag_168h", "rolling_24h", "rolling_7d"]
TARGET = "COMED"

def split_xy(data):
    X = data[FEATURES]
    y = data[TARGET]
    return X, y

X1, y1 = split_xy(client_1_fe)
X2, y2 = split_xy(client_2_fe)


# ================================
# 8. Train Models
# ================================
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
}

def train_and_evaluate(X, y, model):
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return {
        "MAE": mean_absolute_error(y_test, preds),
        "RMSE": np.sqrt(mean_squared_error(y_test, preds)),
        "R2": r2_score(y_test, preds)
    }


# ================================
# 9. Model Evaluation
# ================================
results = {}

for client_name, (X, y) in {
    "Client 1": (X1, y1),
    "Client 2": (X2, y2)
}.items():
    results[client_name] = {}
    for model_name, model in models.items():
        results[client_name][model_name] = train_and_evaluate(X, y, model)

results_df = pd.DataFrame(results)
print(results_df)


# ================================
# 10. Analysis (Discussion Summary)
# ================================
"""
