import sumolib
import pandas as pd
import xml.etree.ElementTree as ET

NET_FILE = "simulation_map.net.xml"
TRIPINFO_FILE = "tripinfo_adaptive.xml"

print("Generating ADAPTIVE datasets...")

net = sumolib.net.readNet(NET_FILE)
rows = []

for edge in net.getEdges():
    if edge.isSpecial():
        continue

    rows.append({
        "edge_id": edge.getID(),
        "from_node": edge.getFromNode().getID(),
        "to_node": edge.getToNode().getID(),
        "num_lanes": edge.getLaneNumber(),
        "speed_limit": edge.getSpeed(),
        "priority": edge.getPriority()
    })

pd.DataFrame(rows).to_csv("component1_network_adaptive.csv", index=False)

tree = ET.parse(TRIPINFO_FILE)
root = tree.getroot()

c2, c4 = [], []

for trip in root.findall("tripinfo"):
    duration = float(trip.get("duration"))
    waiting = float(trip.get("waitingTime"))
    route = float(trip.get("routeLength"))
    loss = float(trip.get("timeLoss"))

    c2.append({
        "vehicle_id": trip.get("id"),
        "depart_time": float(trip.get("depart")),
        "arrival_time": float(trip.get("arrival")),
        "duration": duration,
        "waiting_time": waiting,
        "route_length": route,
        "time_loss": loss
    })

    c4.append({
        "vehicle_id": trip.get("id"),
        "duration": duration,
        "waiting_time": waiting,
        "time_loss": loss,
        "route_length": route,
        "average_speed": route / duration if duration > 0 else 0,
        "waiting_ratio": waiting / duration if duration > 0 else 0,
        "delay_ratio": loss / duration if duration > 0 else 0
    })

pd.DataFrame(c2).to_csv("component2_traffic_adaptive.csv", index=False)
pd.DataFrame(c4).to_csv("component4_performance_adaptive.csv", index=False)

print("✅ Adaptive datasets ready")
