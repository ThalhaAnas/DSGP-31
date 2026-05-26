import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("final_dataset_fixed.csv")

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
# Define congestion if waiting ratio > 10%

df["congestion"] = (df["waiting_ratio"] > 0.10).astype(int)

# -----------------------------
# Feature Selection
# -----------------------------
features = [
    "depart_time",
    "waiting_time",
    "time_loss",
    "route_length",
    "average_speed",
    "waiting_ratio",
    "delay_ratio"
]

target = "congestion"

X = df[features]
y = df[target]

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
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
df.to_csv("processed_fixed_dataset.csv", index=False)

print("\nProcessed dataset saved as 'processed_fixed_dataset.csv'")