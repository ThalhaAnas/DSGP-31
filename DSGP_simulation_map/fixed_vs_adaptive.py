import pandas as pd
import matplotlib.pyplot as plt
import re

# ===============================
# INPUT FILES
# ===============================

FIXED = "component4_performance_fixed.csv"
ADAPTIVE = "component4_performance_adaptive.csv"

df_f = pd.read_csv(FIXED)
df_a = pd.read_csv(ADAPTIVE)

# ===============================
# KPI DEFINITIONS
# ===============================

kpis = {
    "Average Waiting Time (s)": "waiting_time",
    "Average Time Loss (s)": "time_loss",
    "Average Speed (m/s)": "average_speed",
    "Waiting Ratio": "waiting_ratio",
    "Delay Ratio": "delay_ratio"
}

rows = []

# ===============================
# HELPER: SAFE FILENAME
# ===============================

def safe_filename(name):
    """
    Converts KPI name into a Windows-safe filename
    """
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)   # remove special chars
    name = name.replace(" ", "_")
    return name


# ===============================
# KPI COMPARISON + PLOTS
# ===============================

for name, col in kpis.items():
    f = df_f[col].mean()
    a = df_a[col].mean()

    rows.append({
        "KPI": name,
        "Fixed": f,
        "Adaptive": a,
        "Difference (Fixed - Adaptive)": f - a
    })

    # Plot
    plt.figure()
    plt.bar(["Fixed-Time", "Adaptive"], [f, a])
    plt.title(name)
    plt.ylabel(name)
    plt.tight_layout()

    filename = safe_filename(name) + ".png"
    plt.savefig(filename)
    plt.show()

    print(f"📊 Saved graph: {filename}")

# ===============================
# SAVE SUMMARY CSV
# ===============================

pd.DataFrame(rows).to_csv("kpi_comparison_summary.csv", index=False)
print("\n✅ KPI comparison complete. Summary saved.")
