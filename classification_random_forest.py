import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

df = pd.read_csv("component1_enriched_fixed.csv")

features = ["vehicle_count", "avg_waiting_time", "avg_time_loss"]

X = df[features]
y = df["is_high_traffic"]

#split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

#Train model

rf = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=10,
                            class_weight="balanced", random_state=42, n_jobs=-1)

rf.fit(X_train, y_train)