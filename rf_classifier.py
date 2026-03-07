import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

# Load Dataset
df = pd.read_csv("processed_dynamic_dataset.csv")

# Remove non-numeric columns
df = df.drop(columns=["system_type"], errors="ignore")

# Define Features & Target
X = df.drop("is_congested", axis=1)
y = df["is_congested"]