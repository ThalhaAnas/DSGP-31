import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

#Load  dataset
df = pd.read_csv("component1_merged.csv")

#encode system type
df["system_encoded"] = df["system_type"].map({
    "fixed": 0,
    "adaptive": 1
})

features = [
    "vehicle_count",
    "avg_time_loss",
    "system_encoded"
]

X = df[features]
y = df["avg_waiting_time"]

#train, test data split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)

# Train model
rf = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

#evaluation
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Random Forest Regression Results:")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.3f}")

#check feature importance
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance_df)
