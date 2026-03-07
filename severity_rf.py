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