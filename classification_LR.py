import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("component1_enriched_fixed.csv")

print(df.columns)
print(df.head())

# Select features and target

features = ["vehicle_count", "avg_waiting_time", "avg_time_loss"]

x = df[features]
y = df["is_high_traffic"]

# split training n=and testing data

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42, stratify=y)

# Feature scaling

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression Model

log_reg = LogisticRegression(class_weight="balanced", max_iter=1000)

log_reg.fit(X_train_scaled, y_train)