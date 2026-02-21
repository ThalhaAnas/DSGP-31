import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

df = pd.read_csv("component1_merged.csv")

df["system_encoded"] = df["system_type"].map({
    "fixed": 0,
    "adaptive": 1
})

features = ["vehicle_count", "avg_waiting_time", "avg_time_loss", "system_encoded"]

X = df[features]
y = df["is_high_traffic"]

#split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

#Train model

rf = RandomForestClassifier(n_estimators=300, max_depth=12, min_samples_split=10,
                            class_weight="balanced", random_state=42, n_jobs=-1)

rf.fit(X_train, y_train)


#model evaluation

y_pred = rf.predict(X_test)

print("\nConfusion Matrix(Random Forest):")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report(Random Forest):")
print(classification_report(y_test, y_pred))

#feature importance

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("Feature Importance(Random Forest):")
print(importance_df)