import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("component1_merged.csv")

df["system_encoded"] = df["system_type"].map({
    "fixed": 0,
    "adaptive": 1
})


# Select features and target

features = ["vehicle_count", "avg_waiting_time", "avg_time_loss", "system_encoded"]

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

# Evaluate model
y_pred = log_reg.predict(X_test_scaled)

print("Confusion Matrix (Logistic Regression):")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report (Logistic Regression):")
print(classification_report(y_test, y_pred))

#Interpret coefficients
#Helps to identify factors that increase congestion risk, which matter most

coef_df = pd.DataFrame({
    "Feature": features,
    "Coefficient": log_reg.coef_[0]
})

print(coef_df)
