import pandas as pd

print(" Merging Component 1 datasets...")


# LOAD DATASETS


fixed = pd.read_csv("component1_enriched_fixed.csv")
adaptive = pd.read_csv("component1_enriched_adaptive.csv")

print("✔ Fixed shape   :", fixed.shape)
print("✔ Adaptive shape:", adaptive.shape)

# BASIC SANITY CHECK

# Ensure same columns
assert list(fixed.columns) == list(adaptive.columns), \
    " Column mismatch between fixed and adaptive datasets"

print("✔ Columns match")

# MERGE (ROW-WISE CONCAT)

merged = pd.concat([fixed, adaptive], ignore_index=True)

print("✔ Merged shape:", merged.shape)

# OPTIONAL: SORT FOR READABILITY

merged = merged.sort_values(by=["system_type", "traffic_score"], ascending=[True, False])

# SAVE

OUTPUT_FILE = "component1_merged.csv"
merged.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Component 1 merged dataset saved as {OUTPUT_FILE}")
