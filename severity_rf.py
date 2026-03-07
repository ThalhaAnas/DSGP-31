import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load Dataset
df = pd.read_csv("final_dataset_dynamic.csv")

# Create Congestion Severity
def severity_level(ratio):
    if ratio <= 0.10:    # Low congestion
        return 0
    elif ratio <= 0.25:  # Medium congestion
        return 1
    else:                # High congestion
        return 2

df["congestion_level"] = df["waiting_ratio"].apply(severity_level)

print("\nClass Distribution:")
print(df["congestion_level"].value_counts())

# Remove Leakage Columns
df = df.drop(columns=[
    "vehicle_id",
    "arrival_time",
    "duration",
    "waiting_time",
    "waiting_ratio",
    "delay_ratio",
    "is_congested",
    "system_type"
], errors="ignore")

# Define Features & Target
X = df.drop("congestion_level", axis=1)
y = df["congestion_level"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# Train Random Forest
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=10,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

# Prediction
y_pred = rf.predict(X_test)

# Evaluation
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Plot Confusion Matrix
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens")
plt.title("Severity Prediction Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Feature Importance
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance_df)

sns.barplot(x="Importance", y="Feature", data=importance_df)
plt.title("Severity Model Feature Importance")
plt.show()