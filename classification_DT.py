import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("component1_enriched_fixed.csv")

#select features

features = ["vehicle_count", "avg_waiting_time", "avg_time_loss"]

X = df[features]
y = df["is_high traffic"]

#train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)