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

