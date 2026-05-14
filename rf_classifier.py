import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# -----------------------------
# LOAD DATASET
# -----------------------------
df = pd.read_csv("processed_dynamic_dataset.csv")

# Remove non-numeric columns
df = df.drop(columns=["system_type"], errors="ignore")

# -----------------------------
# SELECT FEATURES (IMPORTANT)
# -----------------------------
features = [
    "depart_time",
    "time_loss",
    "route_length",
    "average_speed"
]

X = df[features]
y = df["is_congested"]

print("Features used by model:")
print(X.columns)

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# -----------------------------
# TRAIN RANDOM FOREST
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=10,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

# -----------------------------
# PREDICTIONS
# -----------------------------
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:,1]

# -----------------------------
# EVALUATION
# -----------------------------
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

auc_score = roc_auc_score(y_test, y_prob)
print("\nROC AUC Score:", auc_score)

# -----------------------------
# CONFUSION MATRIX PLOT
# -----------------------------
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Binary Congestion Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance_df)

sns.barplot(x="Importance", y="Feature", data=importance_df)
plt.title("Feature Importance")
plt.show()

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(rf, "dynamic_congestion_prediction.pkl")

print("\nCongestion model saved successfully!")