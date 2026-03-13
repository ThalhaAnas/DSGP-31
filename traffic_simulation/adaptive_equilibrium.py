import traci
import pandas as pd



SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "simulation_map.sumocfg"

SIM_END = 3600
LOG_INTERVAL = 30

# Signal limits
MAX_ADJUST = 0.05
MIN_GREEN = 5

# Pressure weights
WAITING_WEIGHT = 0.5



# Road Priority Weighting

def get_lane_priority(lane):

    """
    road priority weighting using SUMO edge priority.
    """

    edge = traci.lane.getEdgeID(lane)

    try:
        priority = traci.edge.getPriority(edge)
    except:
        priority = 1

    # Normalize priority weight
    if priority >= 3:
        return 2.0      # Main road
    elif priority == 2:
        return 1.5      # Medium road
    else:
        return 1.0      # Minor road



# Junction Pressure Calculation

def junction_pressure(tls):

    """
    Pressure = (Queue × Priority Weight) + Waiting Time Factor
    """

    lanes = traci.trafficlight.getControlledLanes(tls)

    pressure = 0

    for lane in lanes:

        waiting_vehicles = traci.lane.getLastStepHaltingNumber(lane)
        waiting_time = traci.lane.getWaitingTime(lane)

        priority_weight = get_lane_priority(lane)

        pressure += (waiting_vehicles * priority_weight) + (waiting_time * WAITING_WEIGHT)

    return pressure


# Simulation Controller

def run():

    traci.start([
        SUMO_BINARY,
        "-c",
        SUMO_CONFIG,
        "--tripinfo-output",
        "tripinfo_adaptive.xml"
    ])

    tls_ids = traci.trafficlight.getIDList()

    signal_log = []

    time = 0

    while time < SIM_END:

        traci.simulationStep()
        time += 1

        if time % LOG_INTERVAL != 0:
            continue

        # Network pressure
        pressures = {tls: junction_pressure(tls) for tls in tls_ids}

        avg_pressure = sum(pressures.values()) / len(pressures)

        # Adaptive signal control
        for tls in tls_ids:

            logic = traci.trafficlight.getAllProgramLogics(tls)[0]

            greens = [p for p in logic.phases if "G" in p.state]

            if not greens:
                continue

            main_green = max(greens, key=lambda p: p.duration)

            delta = max(1, int(main_green.duration * MAX_ADJUST))

            # Adaptive timing logic
            if pressures[tls] > avg_pressure:
                main_green.duration += delta
            else:
                main_green.duration = max(
                    MIN_GREEN,
                    main_green.duration - delta
                )

            traci.trafficlight.setProgramLogic(tls, logic)

            # Logging
            signal_log.append({
                "time": time,
                "traffic_light": tls,
                "phase_duration": main_green.duration,
                "junction_pressure": pressures[tls],
                "avg_network_pressure": avg_pressure
            })

    traci.close()

    df = pd.DataFrame(signal_log)
    df.to_csv("adaptive_signal_log.csv", index=False)

    print("Simulation finished ")



# Run

if __name__ == "__main__":
    run()