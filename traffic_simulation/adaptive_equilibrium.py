import traci
import pandas as pd

"""
ADAPTIVE EQUILIBRIUM-BASED CONTROLLER

- Measures congestion at all junctions
- Computes network average pressure
- Adjusts green times to balance load
"""

SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "simulation_map.sumocfg"

SIM_END = 3600
LOG_INTERVAL = 30
MAX_ADJUST = 0.05
MIN_GREEN = 5

def junction_pressure(tls):
    lanes = traci.trafficlight.getControlledLanes(tls)
    return sum(traci.lane.getLastStepHaltingNumber(l) for l in lanes)

def run():
    traci.start([
        SUMO_BINARY,
        "-c", SUMO_CONFIG,
        "--tripinfo-output", "tripinfo_adaptive.xml"
    ])

    tls_ids = traci.trafficlight.getIDList()
    signal_log = []

    time = 0
    while time < SIM_END:
        traci.simulationStep()
        time += 1

        if time % LOG_INTERVAL != 0:
            continue