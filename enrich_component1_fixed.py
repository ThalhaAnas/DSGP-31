import xml.etree.ElementTree as ET
import pandas as pd

# FILE PATHS (FIXED SYSTEM)


NETWORK_FILE = "component1_network_fixed.csv"
TRIPINFO_FILE = "tripinfo_fixed.xml"
ROUTE_FILE = "simulation_map.rou.xml"
OUTPUT_FILE = "component1_enriched_fixed.csv"

print("🔵 Enriching Component 1 (FIXED)...")

# LOAD NETWORK DATA


df = pd.read_csv(NETWORK_FILE)

# Initialize enrichment columns
df["vehicle_count"] = 0
df["avg_waiting_time"] = 0.0
df["avg_time_loss"] = 0.0

# LOAD TRIPINFO (VEHICLE METRICS)

trip_metrics = {}

tree = ET.parse(TRIPINFO_FILE)
root = tree.getroot()

for trip in root.findall("tripinfo"):
    trip_metrics[trip.get("id")] = {
        "waiting": float(trip.get("waitingTime")),
        "loss": float(trip.get("timeLoss"))
    }

print(f"✔ Loaded trip metrics for {len(trip_metrics)} vehicles")

# PARSE ROUTES (CORRECT STRUCTURE)

edge_stats = {}

tree = ET.parse(ROUTE_FILE)
root = tree.getroot()

vehicle_count = 0

for veh in root.findall("vehicle"):
    veh_id = veh.get("id")

    # IMPORTANT: route is a child element, NOT an attribute
    route_elem = veh.find("route")
    if route_elem is None:
        continue

    route = route_elem.get("edges", "")
    if not route:
        continue

    if veh_id not in trip_metrics:
        continue

    wait = trip_metrics[veh_id]["waiting"]
    loss = trip_metrics[veh_id]["loss"]

    edges = route.split()
    vehicle_count += 1

    for edge in edges:
        # Skip internal edges
        if edge.startswith(":"):
            continue

        if edge not in edge_stats:
            edge_stats[edge] = {
                "count": 0,
                "wait": 0.0,
                "loss": 0.0
            }

        edge_stats[edge]["count"] += 1
        edge_stats[edge]["wait"] += wait
        edge_stats[edge]["loss"] += loss

print(f"✔ Processed routes for {vehicle_count} vehicles")
print(f"✔ Collected stats for {len(edge_stats)} edges")

# MAP EDGE STATS TO NETWORK

mapped_edges = 0

for idx, row in df.iterrows():
    edge_id = row["edge_id"]

    if edge_id in edge_stats:
        stats = edge_stats[edge_id]
        df.at[idx, "vehicle_count"] = stats["count"]
        df.at[idx, "avg_waiting_time"] = stats["wait"] / stats["count"]
        df.at[idx, "avg_time_loss"] = stats["loss"] / stats["count"]
        mapped_edges += 1

print(f"✔ Mapped traffic data to {mapped_edges} network edges")

# TRAFFIC SCORING

df["traffic_score"] = (
    df["vehicle_count"] * 0.5 +
    df["avg_waiting_time"] * 0.3 +
    df["avg_time_loss"] * 0.2
)

# TRAFFIC LEVEL CLASSIFICATION

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

# SAVE OUTPUT

df.to_csv(OUTPUT_FILE, index=False)

print("✅ Component 1 FIXED enrichment complete")
print(f"Saved as: {OUTPUT_FILE}")
