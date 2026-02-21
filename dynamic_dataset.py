import pandas as pd
import xml.etree.ElementTree as ET


# ===============================
# CONFIGURATION
# ===============================

SYSTEM_TYPE = "dynamic"
TRIPINFO_FILE = "tripinfo_dynamic.xml"
OUTPUT_FILE = "final_dataset_dynamic.csv"

print("Generating DYNAMIC unified dataset...")

# ===============================
# PARSE TRIPINFO
# ===============================

tree = ET.parse(TRIPINFO_FILE)
root = tree.getroot()

rows = []

for trip in root.findall("tripinfo"):

    duration = float(trip.get("duration"))
    waiting = float(trip.get("waitingTime"))
    route_len = float(trip.get("routeLength"))
    loss = float(trip.get("timeLoss"))

    rows.append({
        "vehicle_id": trip.get("id"),
        "system_type": SYSTEM_TYPE,

        "depart_time": float(trip.get("depart")),
        "arrival_time": float(trip.get("arrival")),
        "duration": duration,

        "waiting_time": waiting,
        "time_loss": loss,
        "route_length": route_len,

        "average_speed": route_len / duration if duration > 0 else 0,
        "waiting_ratio": waiting / duration if duration > 0 else 0,
        "delay_ratio": loss / duration if duration > 0 else 0
    })

# ===============================
# SAVE DATASET
# ===============================

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Dynamic dataset saved:", OUTPUT_FILE)
