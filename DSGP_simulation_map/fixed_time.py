import traci
import pandas as pd

"""
FIXED-TIME TRAFFIC SIGNAL CONTROLLER (TUNED BASELINE)

- Static (non-adaptive)
- Different green times for major vs minor junctions
- Reflects real-world fixed-time signal plans
- Acts as a FAIR baseline for comparison
"""

# ===============================
# CONFIGURATION
# ===============================

SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "simulation_map.sumocfg"

SIM_END = 3600           # 1 hour simulation
LOG_INTERVAL = 30        # log signal behaviour every 30 seconds

# Fixed-time parameters (tuned, realistic)
MAJOR_GREEN = 55         # major junctions
MEDIUM_GREEN = 45        # medium junctions
MINOR_GREEN = 30         # minor junctions

MAJOR_YELLOW = 4
MEDIUM_YELLOW = 4
MINOR_YELLOW = 3


def run():
    # Start SUMO
    traci.start([
        SUMO_BINARY,
        "-c", SUMO_CONFIG,
        "--tripinfo-output", "tripinfo_fixed.xml"
    ])

    traffic_lights = traci.trafficlight.getIDList()
    signal_log = []

    print("Tuned fixed-time started. TLS count:", len(traffic_lights))

