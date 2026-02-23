import pandas as pd
import os

print("--- STEP 1: FEATURE ENGINEERING ---")

# Load the Adaptive Runtime data (The "Smart" Data)
df = pd.read_csv('component3_control_adaptive_runtime.csv')

# Select Features (Inputs) and Target (Output)
features = ['green_count', 'red_count', 'junction_pressure', 'average_network_pressure']
target = 'phase_duration'

# Cleaning: Drop rows with missing values to ensure clean training data
model_df = df[features + [target]].dropna()

# Save processed data for the next step
model_df.to_csv('traffic_training_data.csv', index=False)

print(f"Data Cleaned. Rows: {len(model_df)}")
print("Saved to: traffic_training_data.csv")