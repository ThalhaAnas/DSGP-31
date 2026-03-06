import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# Load dataset
df = pd.read_csv("final_dataset_dynamic.csv")

print("\nColumns:")
print(df.columns)

print("\nSummary Statistics:")
print(df.describe())

# -----------------------------
# 1️⃣ Trip Duration Distribution
# -----------------------------
plt.figure(figsize=(12,6))
sns.histplot(df["duration"], bins=40, kde=True)
plt.title("Trip Duration Distribution")
plt.xlabel("Duration (seconds)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# -----------------------------
# 2️⃣ Waiting Time Distribution
# -----------------------------
plt.figure(figsize=(12,6))
sns.histplot(df["waiting_time"], bins=40, kde=True)
plt.title("Waiting Time Distribution")
plt.xlabel("Waiting Time (seconds)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# -----------------------------
# 3️⃣ Time Loss Distribution
# -----------------------------
plt.figure(figsize=(12,6))
sns.histplot(df["time_loss"], bins=40, kde=True)
plt.title("Time Loss Distribution")
plt.xlabel("Time Loss (seconds)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# -----------------------------
# 4️⃣ Correlation Heatmap
# -----------------------------
plt.figure(figsize=(10,8))
corr = df.corr(numeric_only=True)

sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# -----------------------------
# 5️⃣ Waiting Time vs Duration
# -----------------------------
plt.figure(figsize=(12,6))
sns.scatterplot(x="duration", y="waiting_time", data=df, alpha=0.4)
sns.regplot(x="duration", y="waiting_time", data=df, scatter=False, color="red")
plt.title("Waiting Time vs Trip Duration")
plt.tight_layout()
plt.show()

# -----------------------------
# 6️⃣ Speed vs Delay
# -----------------------------
plt.figure(figsize=(12,6))
sns.scatterplot(x="average_speed", y="delay_ratio", data=df, alpha=0.4)
sns.regplot(x="average_speed", y="delay_ratio", data=df, scatter=False, color="red")
plt.title("Average Speed vs Delay Ratio")
plt.tight_layout()
plt.show()

# -----------------------------
# 7️⃣ Congestion Over Time
# -----------------------------
plt.figure(figsize=(12,6))
df.groupby("depart_time")["waiting_time"].mean().plot()
plt.title("Average Waiting Time Over Departure Time")
plt.ylabel("Average Waiting Time")
plt.tight_layout()
plt.show()

# -----------------------------
# 8️⃣ System Comparison (if both exist)
# -----------------------------
if "system_type" in df.columns:
    plt.figure(figsize=(10,6))
    sns.boxplot(x="system_type", y="waiting_time", data=df)
    plt.title("Waiting Time Comparison by System Type")
    plt.tight_layout()
    plt.show()

print("\nEDA Completed.")