import traci
import pandas as pd

"""
SCENARIO: POLICE OFFICER OVERRIDE
- Runs adaptive equilibrium logic normally.
- At t=600 to t=780 (3 mins), an officer takes over the first junction.
- Forces a massive green phase (e.g., clearing a VIP convoy or heavy jam).
- Adaptive logic resumes afterward.
"""

SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "simulation_map.sumocfg"

SIM_END = 3600
LOG_INTERVAL = 30
MAX_ADJUST = 0.05
MIN_GREEN = 5

# Override Settings
OVERRIDE_START = 600
OVERRIDE_END = 780

def junction_pressure(tls):
    lanes = traci.trafficlight.getControlledLanes(tls)
    return sum(traci.lane.getLastStepHaltingNumber(l) for l in lanes)


def run():
    traci.start([
        SUMO_BINARY, "-c", SUMO_CONFIG, "--tripinfo-output", "tripinfo_scenario.xml"
    ])

    tls_ids = traci.trafficlight.getIDList()
    target_tls = tls_ids[0]  # The junction the police officer takes over

    print(f"Simulation Started. Police officer will take over {target_tls} at t={OVERRIDE_START}s")


if __name__ == "__main__":
    run()