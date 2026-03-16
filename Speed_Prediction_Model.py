import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib  # Make sure this is imported correctly
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

print("--- INITIALIZING ML SPEED PREDICTOR (MANUAL DATASET) ---")

# 1. Load the new dataset
file_name = "final_dataset_manual.csv"
try:
    df = pd.read_csv(file_name)
    print(f"Successfully loaded {file_name}")
except FileNotFoundError:
    print(f"Error: Cannot find {file_name}. Check if it's in the same folder.")
    exit()

