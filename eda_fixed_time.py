import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
====================================================
FIXED SYSTEM - COMPLETE EDA ANALYSIS
====================================================
This script performs full exploratory data analysis
for the fixed-time traffic signal dataset.

Run after:
1. tripinfo_fixed.xml generated
2. fixed_dataset.py executed
3. final_dataset_fixed.csv created
====================================================
"""

DATA_FILE = "final_dataset_fixed.csv"

# ====================================================
# LOAD DATA
# ====================================================

print("Loading dataset...")
df = pd.read_csv(DATA_FILE)

print("\nDataset Shape:", df.shape)
print("\nFirst 5 Rows:\n", df.head())

print("\nStatistical Summary:\n")
print(df.describe())

# ====================================================
# 1️⃣ TRIP DURATION DISTRIBUTION
# ====================================================

plt.figure()
plt.hist(df["duration"], bins=30)
plt.title("Trip Duration Distribution (Fixed System)")
plt.xlabel("Duration (seconds)")
plt.ylabel("Number of Vehicles")
plt.grid(True)
plt.show()

# ====================================================
# 2️⃣ WAITING TIME DISTRIBUTION
# ====================================================

plt.figure()
plt.hist(df["waiting_time"], bins=30)
plt.title("Waiting Time Distribution")
plt.xlabel("Waiting Time (seconds)")
plt.ylabel("Number of Vehicles")
plt.grid(True)
plt.show()

# ====================================================
# 3️⃣ AVERAGE SPEED DISTRIBUTION
# ====================================================

plt.figure()
plt.hist(df["average_speed"], bins=30)
plt.title("Average Speed Distribution")
plt.xlabel("Speed (m/s)")
plt.ylabel("Number of Vehicles")
plt.grid(True)
plt.show()

# ====================================================
# 4️⃣ WAITING TIME VS DURATION
# ====================================================

plt.figure()
plt.scatter(df["duration"], df["waiting_time"])
plt.title("Waiting Time vs Trip Duration")
plt.xlabel("Duration (seconds)")
plt.ylabel("Waiting Time (seconds)")
plt.grid(True)
plt.show()

# ====================================================
# 5️⃣ ROUTE LENGTH VS WAITING TIME
# ====================================================

plt.figure()
plt.scatter(df["route_length"], df["waiting_time"])
plt.title("Route Length vs Waiting Time")
plt.xlabel("Route Length (meters)")
plt.ylabel("Waiting Time (seconds)")
plt.grid(True)
plt.show()

# ====================================================
# 6️⃣ CORRELATION HEATMAP
# ====================================================

numeric_df = df.drop(columns=["vehicle_id", "system_type"])
corr = numeric_df.corr()

plt.figure()
plt.imshow(corr)
plt.title("Correlation Matrix - Fixed System")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.colorbar()
plt.show()

# ====================================================
# 7️⃣ OUTLIER DETECTION (BOXPLOT)
# ====================================================

plt.figure()
plt.boxplot([df["duration"], df["waiting_time"], df["time_loss"]])
plt.xticks([1, 2, 3], ["Duration", "Waiting Time", "Time Loss"])
plt.title("Outlier Detection")
plt.grid(True)
plt.show()

# ====================================================
# 8️⃣ CONGESTION TREND OVER TIME
# ====================================================

df_sorted = df.sort_values("depart_time")

plt.figure()
plt.plot(df_sorted["depart_time"], df_sorted["duration"])
plt.title("Trip Duration Over Departure Time")
plt.xlabel("Departure Time")
plt.ylabel("Trip Duration")
plt.grid(True)
plt.show()

# ====================================================
# PERFORMANCE SUMMARY
# ====================================================

print("\n========== FIXED SYSTEM PERFORMANCE ==========")
print("Average Duration:", round(df["duration"].mean(), 2))
print("Average Waiting Time:", round(df["waiting_time"].mean(), 2))
print("Average Time Loss:", round(df["time_loss"].mean(), 2))
print("Average Speed:", round(df["average_speed"].mean(), 2))
print("Average Waiting Ratio:", round(df["waiting_ratio"].mean(), 3))
print("Average Delay Ratio:", round(df["delay_ratio"].mean(), 3))
print("==============================================")