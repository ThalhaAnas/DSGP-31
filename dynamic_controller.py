import traci
import pandas as pd

SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "simulation_map.sumocfg"
SIM_END = 3600

MIN_GREEN = 10
MAIN_CLEAR_THRESHOLD = 5
SIDE_QUEUE_THRESHOLD = 8
SIDE_RELIEF_TIME = 25

DOWNSTREAM_FACTOR = 1.5   # Downstream must be 50% worse to trigger
REDUCE_STEP = 3           # Gentle green reduction


def get_lane_queue(lanes):
    return sum(traci.lane.getLastStepHaltingNumber(l) for l in lanes)


def classify_lanes(tls_id):

    lanes = traci.trafficlight.getControlledLanes(tls_id)
    edge_map = {}

    for lane in lanes:
        edge = lane.split("_")[0]
        edge_map.setdefault(edge, []).append(lane)

    sorted_edges = sorted(edge_map.items(),
                          key=lambda x: len(x[1]),
                          reverse=True)

    main_lanes = []
    side_lanes = []

    if sorted_edges:
        main_lanes = sorted_edges[0][1]
        for _, lns in sorted_edges[1:]:
            side_lanes.extend(lns)

    return main_lanes, side_lanes

def get_downstream_pressure(lanes):
    """
    Stable downstream approximation:
    Count halted vehicles on main edges
    """
    pressure = 0
    for lane in lanes:
        edge = lane.split("_")[0]
        pressure += traci.edge.getLastStepHaltingNumber(edge)
    return pressure


# ===============================
# MAIN CONTROLLER
# ===============================

def run():

    traci.start([
        SUMO_BINARY,
        "-c", SUMO_CONFIG,
        "--tripinfo-output", "tripinfo_dynamic.xml"
    ])

    tls_ids = traci.trafficlight.getIDList()

    print("Dynamic (tuned) started. Junctions:", len(tls_ids))

    time = 0

    while time < SIM_END:

        traci.simulationStep()
        time += 1

        for tls in tls_ids:

            logic = traci.trafficlight.getAllProgramLogics(tls)[0]
            phases = logic.phases

            greens = [p for p in phases if "G" in p.state]
            if not greens:
                continue

            main_green = max(greens, key=lambda p: p.duration)

            main_lanes, side_lanes = classify_lanes(tls)

            main_queue = get_lane_queue(main_lanes)
            side_queue = get_lane_queue(side_lanes)
            downstream = get_downstream_pressure(main_lanes)

            # =====================================================
            # STEP 1: APPLY MANUAL BASE LOGIC
            # =====================================================

            if main_queue > MAIN_CLEAR_THRESHOLD and side_queue < SIDE_QUEUE_THRESHOLD:
                main_green.duration += 5

            elif side_queue >= SIDE_QUEUE_THRESHOLD:
                main_green.duration = max(MIN_GREEN, SIDE_RELIEF_TIME)

            else:
                main_green.duration = max(MIN_GREEN, main_green.duration)

            # =====================================================
            # STEP 2: DOWNSTREAM PROTECTION (ONLY IF SEVERE)
            # =====================================================

            if downstream > main_queue * DOWNSTREAM_FACTOR:
                main_green.duration = max(
                    MIN_GREEN,
                    main_green.duration - REDUCE_STEP
                )

            traci.trafficlight.setProgramLogic(tls, logic)

    traci.close()

    print("✅ Dynamic simulation finished at 3600 seconds")


if __name__ == "__main__":
    run()