import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("component1_merged.csv")

#select features

df["system_encoded"] = df["system_type"].map({
    "fixed": 0,
    "adaptive": 1
})

features = ["vehicle_count", "avg_waiting_time", "avg_time_loss", "system_encoded"]

X = df[features]
y = df["is_high_traffic"]

#train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

#Train DT model

dt = DecisionTreeClassifier(
    max_depth=6,
    min_samples_leaf=20,
    class_weight="balanced",
    random_state=42,
)

dt.fit(X_train, y_train)

#Evaluation
y_pred = dt.predict(X_test)

print("Confusion Matrix (Decision Tree):")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report (Decision Tree):")
print(classification_report(y_test, y_pred))

#feature importance

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": dt.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance_df)