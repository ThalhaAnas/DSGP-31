import xml.etree.ElementTree as ET
import pandas as pd

# ===============================
# INPUT FILES (FIXED)
# ===============================

NETWORK_FILE = "component1_network_fixed.csv"
TRIPINFO_FILE = "tripinfo_fixed.xml"
ROUTE_FILE = "simulation_map.rou.xml"
OUTPUT_FILE = "component1_enriched_fixed.csv"

print("🔵 Enriching Component 1 (FIXED)...")

# ===============================
# LOAD NETWORK DATA
# ===============================

df = pd.read_csv(NETWORK_FILE)

df["vehicle_count"] = 0
df["avg_waiting_time"] = 0.0
df["avg_time_loss"] = 0.0

# ===============================
# LOAD TRIP METRICS
# ===============================

trip_metrics = {}

tree = ET.parse(TRIPINFO_FILE)
root = tree.getroot()

for trip in root.findall("tripinfo"):
    trip_metrics[trip.get("id")] = {
        "waiting": float(trip.get("waitingTime")),
        "loss": float(trip.get("timeLoss"))
    }

# ===============================
# PARSE ROUTES
# ===============================

edge_stats = {}

tree = ET.parse(ROUTE_FILE)
root = tree.getroot()

for veh in root.findall("vehicle"):
    veh_id = veh.get("id")
    route = veh.get("route", "")

    if veh_id not in trip_metrics:
        continue

    wait = trip_metrics[veh_id]["waiting"]
    loss = trip_metrics[veh_id]["loss"]

    edges = route.split()

    for edge in edges:
        if edge.startswith(":"):
            continue

        if edge not in edge_stats:
            edge_stats[edge] = {"count": 0, "wait": 0.0, "loss": 0.0}

        edge_stats[edge]["count"] += 1
        edge_stats[edge]["wait"] += wait
        edge_stats[edge]["loss"] += loss

# ===============================
# MAP TO NETWORK
# ===============================

for idx, row in df.iterrows():
    edge_id = row["edge_id"]

    if edge_id in edge_stats:
        stats = edge_stats[edge_id]
        df.at[idx, "vehicle_count"] = stats["count"]
        df.at[idx, "avg_waiting_time"] = stats["wait"] / stats["count"]
        df.at[idx, "avg_time_loss"] = stats["loss"] / stats["count"]

# ===============================
# TRAFFIC SCORING
# ===============================

df["traffic_score"] = (
    df["vehicle_count"] * 0.5 +
    df["avg_waiting_time"] * 0.3 +
    df["avg_time_loss"] * 0.2
)

q50 = df["traffic_score"].quantile(0.5)
q80 = df["traffic_score"].quantile(0.8)

def classify(score):
    if score < q50:
        return "low"
    elif score < q80:
        return "medium"
    else:
        return "high"

df["traffic_level"] = df["traffic_score"].apply(classify)
df["is_high_traffic"] = (df["traffic_level"] == "high").astype(int)

df["system_type"] = "fixed"

# ===============================
# SAVE
# ===============================

df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Fixed enrichment complete → {OUTPUT_FILE}")
