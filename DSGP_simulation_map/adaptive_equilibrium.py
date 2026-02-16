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

        pressures = {tls: junction_pressure(tls) for tls in tls_ids}
        avg_pressure = sum(pressures.values()) / len(pressures)

        for tls in tls_ids:
            logic = traci.trafficlight.getAllProgramLogics(tls)[0]
            greens = [p for p in logic.phases if "G" in p.state]

            if not greens:
                continue

            main_green = max(greens, key=lambda p: p.duration)
            delta = int(main_green.duration * MAX_ADJUST)

            if pressures[tls] > avg_pressure:
                main_green.duration += delta
            else:
                main_green.duration = max(MIN_GREEN, main_green.duration - delta)

            traci.trafficlight.setProgramLogic(tls, logic)

            signal_log.append({
                "time": time,
                "traffic_light_id": tls,
                "phase_duration": main_green.duration,
                "green_count": main_green.state.count("G") + main_green.state.count("g"),
                "yellow_count": main_green.state.count("y"),
                "red_count": main_green.state.count("r"),
                "junction_pressure": pressures[tls],
                "average_network_pressure": avg_pressure,
                "control_type": "adaptive"
            })

    traci.close()

    pd.DataFrame(signal_log).to_csv(
        "component3_control_adaptive_runtime.csv", index=False
    )

    print("Adaptive simulation finished")


if __name__ == "__main__":
    run()
