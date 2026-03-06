import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("final_dataset_dynamic.csv")

print("Initial Shape:", df.shape)

# -----------------------------
# Remove Duplicates
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# Check Missing Values
# -----------------------------
print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna()

# -----------------------------
# Create Congestion Target
# -----------------------------
# Define congestion as waiting ratio > 10%
df["is_congested"] = (df["waiting_ratio"] > 0.15).astype(int)

print("\nClass Distribution:")
print(df["is_congested"].value_counts())

# -----------------------------
# Drop Leakage Columns
# -----------------------------
df = df.drop(columns=[
    "vehicle_id",      # identifier
    "system_type",     # constant
    "arrival_time",    # derived
    "duration",        # contains congestion info
    "waiting_time",    # used in target
    "waiting_ratio",   # used in target
    "delay_ratio"      # derived from waiting/time_loss
])

# -----------------------------
# Define Features & Target
# -----------------------------
X = df.drop("is_congested", axis=1)
y = df["is_congested"]

print("\nRemaining Features:")
print(X.columns)

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# -----------------------------
# Feature Scaling
# -----------------------------
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nPreprocessing Completed.")
print("Training Shape:", X_train_scaled.shape)
print("Test Shape:", X_test_scaled.shape)

# -----------------------------
# Save Processed Dataset
# -----------------------------
df.to_csv("processed_dynamic_dataset.csv", index=False)

print("\nProcessed dataset saved as 'processed_dynamic_dataset.csv'")