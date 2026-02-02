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

    # ===============================
    # APPLY FIXED-TIME SIGNAL PLAN
    # ===============================
    for tls in traffic_lights:
        lanes = traci.trafficlight.getControlledLanes(tls)
        lane_count = len(set(lanes))

        # Classify junction size
        if lane_count >= 8:
            green_time = MAJOR_GREEN
            yellow_time = MAJOR_YELLOW
        elif lane_count >= 4:
            green_time = MEDIUM_GREEN
            yellow_time = MEDIUM_YELLOW
        else:
            green_time = MINOR_GREEN
            yellow_time = MINOR_YELLOW

        logic = traci.trafficlight.getAllProgramLogics(tls)[0]
        phases = logic.phases
        cycle = sum(p.duration for p in phases)

        # Apply fixed timings
        for p in phases:
            if "G" in p.state:
                p.duration = green_time
            elif "y" in p.state or "Y" in p.state:
                p.duration = yellow_time
            else:
                p.duration = max(5, cycle - green_time - yellow_time)

        traci.trafficlight.setProgramLogic(tls, logic)

    # ===============================
    # SIMULATION + RUNTIME LOGGING
    # ===============================
    time = 0
    while time < SIM_END:
        traci.simulationStep()
        time += 1

        if time % LOG_INTERVAL == 0:
            for tls in traffic_lights:
                logic = traci.trafficlight.getAllProgramLogics(tls)[0]
                greens = [p for p in logic.phases if "G" in p.state]

                if not greens:
                    continue

                main_green = max(greens, key=lambda p: p.duration)

                signal_log.append({
                    "time": time,
                    "traffic_light_id": tls,
                    "phase_duration": main_green.duration,
                    "green_count": main_green.state.count("G") + main_green.state.count("g"),
                    "yellow_count": main_green.state.count("y"),
                    "red_count": main_green.state.count("r"),
                    "junction_pressure": None,
                    "average_network_pressure": None,
                    "control_type": "fixed"
                })

    traci.close()

    pd.DataFrame(signal_log).to_csv(
        "component3_control_fixed_runtime.csv", index=False
    )

    print("Fixed-time simulation finished")


if __name__ == "__main__":
    run()
