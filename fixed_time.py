import traci
import pandas as pd
import numpy as np

"""
==========================================================
IMPROVED FIXED-TIME TRAFFIC SIGNAL CONTROLLER (BASELINE)
==========================================================

This controller:

• Uses static pre-defined green times
• Classifies junctions into Major / Medium / Minor
• Applies realistic cycle-based fixed timing
• Logs runtime performance metrics
• Acts as a FAIR baseline for adaptive comparison

This is suitable for academic evaluation & model comparison.
"""

# ==========================================================
# CONFIGURATION SECTION
# ==========================================================

SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "simulation_map.sumocfg"

SIM_END = 3600          # 1 hour simulation
LOG_INTERVAL = 30       # Log every 30 seconds

# Fixed signal timing parameters (Realistic baseline values)
SIGNAL_CONFIG = {
    "MAJOR": {"green": 55, "yellow": 4},
    "MEDIUM": {"green": 45, "yellow": 4},
    "MINOR": {"green": 30, "yellow": 3}
}

MIN_RED = 5   # Minimum safe red duration


# ==========================================================
# HELPER FUNCTION: CLASSIFY JUNCTION SIZE
# ==========================================================

def classify_junction(lane_count):
    """
    Classify junction type based on number of controlled lanes.
    This approximates traffic demand complexity.
    """
    if lane_count >= 8:
        return "MAJOR"
    elif lane_count >= 4:
        return "MEDIUM"
    else:
        return "MINOR"


# ==========================================================
# APPLY FIXED-TIME SIGNAL PLAN
# ==========================================================

def apply_fixed_time_plan(tls_id):
    """
    Modify traffic light program using static cycle logic.
    """

    lanes = traci.trafficlight.getControlledLanes(tls_id)
    lane_count = len(set(lanes))

    # Determine junction category
    junction_type = classify_junction(lane_count)

    green_time = SIGNAL_CONFIG[junction_type]["green"]
    yellow_time = SIGNAL_CONFIG[junction_type]["yellow"]

    logic = traci.trafficlight.getAllProgramLogics(tls_id)[0]
    phases = logic.phases

    # Compute total cycle time
    cycle_time = green_time + yellow_time + MIN_RED

    for phase in phases:

        # Green phase
        if "G" in phase.state or "g" in phase.state:
            phase.duration = green_time

        # Yellow phase
        elif "y" in phase.state or "Y" in phase.state:
            phase.duration = yellow_time

        # Red phase
        else:
            phase.duration = MIN_RED

    traci.trafficlight.setProgramLogic(tls_id, logic)


# ==========================================================
# RUNTIME PERFORMANCE METRICS
# ==========================================================

def compute_network_metrics():
    """
    Compute real-time network performance metrics.
    These are used only for logging and comparison.
    """

    vehicle_ids = traci.vehicle.getIDList()

    total_waiting_time = 0
    total_queue = 0

    for vid in vehicle_ids:
        total_waiting_time += traci.vehicle.getWaitingTime(vid)

        # Queue defined as vehicles moving very slow (<0.1 m/s)
        if traci.vehicle.getSpeed(vid) < 0.1:
            total_queue += 1

    avg_waiting_time = (
        total_waiting_time / len(vehicle_ids)
        if vehicle_ids else 0
    )

    return avg_waiting_time, total_queue


# ==========================================================
# MAIN SIMULATION LOOP
# ==========================================================

def run():

    traci.start([
        SUMO_BINARY,
        "-c", SUMO_CONFIG,
        "--tripinfo-output", "tripinfo_fixed.xml"
    ])

    traffic_lights = traci.trafficlight.getIDList()
    signal_log = []

    print("🚦 Improved Fixed-Time Controller Started")
    print("Traffic Lights Found:", len(traffic_lights))

    # ------------------------------------------------------
    # Apply fixed timing plan to all junctions
    # ------------------------------------------------------
    for tls in traffic_lights:
        apply_fixed_time_plan(tls)

    # ------------------------------------------------------
    # Simulation Execution
    # ------------------------------------------------------
    time = 0
    while time < SIM_END:

        traci.simulationStep()
        time += 1

        # Log performance periodically
        if time % LOG_INTERVAL == 0:

            avg_waiting_time, total_queue = compute_network_metrics()

            for tls in traffic_lights:

                current_phase = traci.trafficlight.getPhase(tls)
                logic = traci.trafficlight.getAllProgramLogics(tls)[0]
                phase_obj = logic.phases[current_phase]

                signal_log.append({
                    "time": time,
                    "traffic_light_id": tls,
                    "current_phase_index": current_phase,
                    "phase_duration": phase_obj.duration,
                    "green_count": phase_obj.state.count("G") + phase_obj.state.count("g"),
                    "yellow_count": phase_obj.state.count("y"),
                    "red_count": phase_obj.state.count("r"),
                    "average_waiting_time": avg_waiting_time,
                    "total_queue_length": total_queue,
                    "control_type": "fixed"
                })

    traci.close()

    pd.DataFrame(signal_log).to_csv(
        "component3_control_fixed_runtime.csv",
        index=False
    )

    print("✅ Fixed-Time Simulation Completed Successfully")


# ==========================================================
# EXECUTION
# ==========================================================

if __name__ == "__main__":
    run()