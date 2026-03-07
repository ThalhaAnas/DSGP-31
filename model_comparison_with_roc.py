import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    accuracy_score
)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("processed_dynamic_dataset.csv")

X = df.drop("is_congested", axis=1)
y = df["is_congested"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# Scale only for Logistic
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# Train Models
# -----------------------------

# Logistic Regression
log_reg = LogisticRegression(class_weight="balanced", max_iter=1000)
log_reg.fit(X_train_scaled, y_train)
log_pred = log_reg.predict(X_test_scaled)
log_probs = log_reg.predict_proba(X_test_scaled)[:, 1]

# Decision Tree
dt = DecisionTreeClassifier(max_depth=6, min_samples_split=20,
                            class_weight="balanced", random_state=42)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
dt_probs = dt.predict_proba(X_test)[:, 1]

# Random Forest
rf = RandomForestClassifier(n_estimators=300, max_depth=10,
                            min_samples_split=10,
                            class_weight="balanced",
                            random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_probs = rf.predict_proba(X_test)[:, 1]

# -----------------------------
# Function to Extract Metrics
# -----------------------------

def get_metrics(y_true, y_pred, y_probs):
    report = classification_report(y_true, y_pred, output_dict=True)
    accuracy = accuracy_score(y_true, y_pred)
    recall = report["1"]["recall"]
    f1 = report["1"]["f1-score"]
    fpr, tpr, _ = roc_curve(y_true, y_probs)
    roc_auc = auc(fpr, tpr)
    return accuracy, recall, f1, roc_auc

# -----------------------------
# Collect Metrics
# -----------------------------

log_metrics = get_metrics(y_test, log_pred, log_probs)
dt_metrics = get_metrics(y_test, dt_pred, dt_probs)
rf_metrics = get_metrics(y_test, rf_pred, rf_probs)

# -----------------------------
# Create Comparison Table
# -----------------------------

comparison_df = pd.DataFrame({
    "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
    "Accuracy": [log_metrics[0], dt_metrics[0], rf_metrics[0]],
    "Recall (Congested)": [log_metrics[1], dt_metrics[1], rf_metrics[1]],
    "F1 (Congested)": [log_metrics[2], dt_metrics[2], rf_metrics[2]],
    "AUC": [log_metrics[3], dt_metrics[3], rf_metrics[3]]
})

print("\n===== MODEL COMPARISON TABLE =====\n")
print(comparison_df)

# -----------------------------
# Plot ROC Curves
# -----------------------------

plt.figure(figsize=(10,7))

for probs, name in zip(
        [log_probs, dt_probs, rf_probs],
        ["Logistic Regression", "Decision Tree", "Random Forest"]):

    fpr, tpr, _ = roc_curve(y_test, probs)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{name} (AUC = {roc_auc:.3f})")

plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.show()