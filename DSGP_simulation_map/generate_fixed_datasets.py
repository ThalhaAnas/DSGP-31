import sumolib
import pandas as pd
import xml.etree.ElementTree as ET

"""
DATASET GENERATOR – FIXED TIME

Generates:
- Component 1: Network
- Component 2: Traffic demand
- Component 4: Performance

Component 3 is runtime-based and already exists.
"""

NET_FILE = "simulation_map.net.xml"
TRIPINFO_FILE = "tripinfo_fixed.xml"

print("Generating FIXED-TIME datasets...")

# ===============================
# COMPONENT 1 — NETWORK
# ===============================
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

pd.DataFrame(rows).to_csv("component1_network_fixed.csv", index=False)