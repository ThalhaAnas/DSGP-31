import pandas as pd

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df = pd.read_csv("component1_network_dataset.csv")
print("===== ORIGINAL SHAPE =====")
print(df.shape)

# -------------------------------------------------------
# 1. Remove duplicates
# -------------------------------------------------------
df = df.drop_duplicates()
print("Removed duplicates. New shape:", df.shape)

# -------------------------------------------------------
# 2. Handle missing values (there should be none)
# -------------------------------------------------------
print("\nMissing values per column:")
print(df.isna().sum())

# No imputations needed because dataset is clean

# -------------------------------------------------------
# 3. Outlier removal (ONLY for columns that make sense)
# -------------------------------------------------------
numeric_cols = [
    "num_lanes",
    "speed_limit",
    "priority",
    "total_length",
    "avg_lane_length",
    "capacity_score",
    "road_importance"
]

def remove_outliers(col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    before = df.shape[0]
    df[col] = df[col].clip(lower, upper)
    after = df.shape[0]
    print(f"Outlier-corrected: {col}")

for col in numeric_cols:
    remove_outliers(col)

# -------------------------------------------------------
# 4. Encode Categorical Column (edge_type)
# -------------------------------------------------------
df["edge_type_encoded"] = df["edge_type"].astype("category").cat.codes

# -------------------------------------------------------
# 5. Save Cleaned Dataset
# -------------------------------------------------------
df.to_csv("component1_network_cleaned.csv", index=False)
print("\n===== CLEANING COMPLETE =====")
print("Saved as: component1_network_cleaned.csv")
