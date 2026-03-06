import traci
import pandas as pd


# ==========================================================
# SUMO CONFIGURATION
# ==========================================================

SUMO_BINARY = "sumo-gui"              # Launch SUMO with graphical interface
SUMO_CONFIG = "simulation_map.sumocfg"  # SUMO configuration file

SIM_END = 3600                       # Simulation duration (1 hour)


# ==========================================================
# SIGNAL TIMING LIMITS
# ==========================================================

MIN_GREEN = 10                       # Minimum green duration allowed
MAX_GREEN = 90                       # Maximum green duration allowed


# ==========================================================
# MANUAL CONTROL PARAMETERS (POLICE STYLE BASE)
# ==========================================================

MAIN_CLEAR_THRESHOLD = 5             # If main road queue exceeds this value,
                                     # traffic police keeps clearing the main road

SIDE_QUEUE_THRESHOLD = 8             # If side road queue exceeds this value,
                                     # the controller temporarily gives priority
                                     # to the side road

SIDE_RELIEF_TIME = 25                # Green duration given to side roads
                                     # when side congestion occurs

# DYNAMIC CONTROL PARAMETERS

DOWNSTREAM_FACTOR = 1.5              # Downstream congestion must be 50% worse
                                     # than the local queue before reducing green

REDUCE_STEP = 3                      # Amount of green time reduction when
                                     # downstream congestion is detected

# HELPER FUNCTION: COUNT QUEUED VEHICLES


def get_lane_queue(lanes):

    """
    Counts how many vehicles are currently halted
    on a given set of lanes.

    traci.lane.getLastStepHaltingNumber(l)
    returns the number of vehicles with speed < 0.1 m/s
    """

    return sum(traci.lane.getLastStepHaltingNumber(l) for l in lanes)


# IMPROVED ROAD CLASSIFICATION

def classify_lanes(tls_id):

    """
    Classifies incoming roads of a junction into:

    MAIN ROAD
    SIDE ROADS

    Instead of using only lane count (which can be misleading),
    this method combines:

    - Edge priority (road importance in SUMO network)
    - Lane count

    This prevents major roads with only 2 lanes from being
    incorrectly classified as side roads.
    """

    lanes = traci.trafficlight.getControlledLanes(tls_id)

    edge_map = {}

    # Group lanes by their edge (road segment)
    for lane in lanes:
        edge = lane.split("_")[0]
        edge_map.setdefault(edge, []).append(lane)

    edge_scores = []

    # Compute a score for each edge
    for edge, lns in edge_map.items():

        try:
            priority = traci.edge.getPriority(edge)  # road importance
        except:
            priority = 1

        lane_count = len(lns)

        # Score = weighted combination of priority and lane count
        score = priority * 2 + lane_count

        edge_scores.append((edge, score, lns))

    # Sort edges by score (highest score = main road)
    edge_scores.sort(key=lambda x: x[1], reverse=True)

    main_lanes = []
    side_lanes = []

    if edge_scores:

        main_lanes = edge_scores[0][2]

        for _, _, lns in edge_scores[1:]:

            side_lanes.extend(lns)

    return main_lanes, side_lanes


# DOWNSTREAM PRESSURE CALCULATION

def get_downstream_pressure(lanes):

    """
    Measures congestion AFTER the intersection.

    If downstream roads are congested,
    sending more vehicles will worsen the traffic.

    This prevents spillback congestion.
    """
    pressure = 0
    for lane in lanes:
        edge = lane.split("_")[0]
        pressure += traci.edge.getLastStepHaltingNumber(edge)
    return pressure


# ==========================================================
# MAIN DYNAMIC CONTROLLER
# ==========================================================

def run():

    # Start SUMO simulation and enable trip logging
    traci.start([
        SUMO_BINARY,
        "-c", SUMO_CONFIG,
        "--tripinfo-output", "tripinfo_dynamic.xml"
    ])

    # Get all traffic lights in the network
    tls_ids = traci.trafficlight.getIDList()

    print("Dynamic controller started. Junctions:", len(tls_ids))

    time = 0


    # MAIN SIMULATION LOOP
    while time < SIM_END:

        traci.simulationStep()   # advance simulation by 1 second
        time += 1

        # Process every traffic signal
        for tls in tls_ids:

            logic = traci.trafficlight.getAllProgramLogics(tls)[0]

            phases = logic.phases

            # Extract phases containing green signals
            greens = [p for p in phases if "G" in p.state]

            if not greens:
                continue

            # Select the longest green phase as the main phase
            main_green = max(greens, key=lambda p: p.duration)

            # Identify main vs side lanes
            main_lanes, side_lanes = classify_lanes(tls)

            # Measure local congestion
            main_queue = get_lane_queue(main_lanes)
            side_queue = get_lane_queue(side_lanes)

            # Measure downstream congestion
            downstream = get_downstream_pressure(main_lanes)

            # ======================================================
            # STEP 1 — POLICE STYLE CONTROL (MANUAL BEHAVIOR)
            # ======================================================

            if main_queue > MAIN_CLEAR_THRESHOLD and side_queue < SIDE_QUEUE_THRESHOLD:

                # Main road heavily congested
                # Police would keep clearing main road

                main_green.duration = min(
                    MAX_GREEN,
                    main_green.duration + 5
                )

            elif side_queue >= SIDE_QUEUE_THRESHOLD:

                # Side roads congested
                # Temporarily give relief

                main_green.duration = max(
                    MIN_GREEN,
                    SIDE_RELIEF_TIME
                )

            else:

                # Maintain stable timing

                main_green.duration = max(
                    MIN_GREEN,
                    main_green.duration
                )

            # ======================================================
            # STEP 2 — DOWNSTREAM PROTECTION
            # ======================================================

            if downstream > main_queue * DOWNSTREAM_FACTOR:

                # Downstream roads are already congested
                # Reduce green to prevent sending more vehicles

                main_green.duration = max(
                    MIN_GREEN,
                    main_green.duration - REDUCE_STEP
                )

            # Apply updated signal timing
            traci.trafficlight.setProgramLogic(tls, logic)

    # End simulation
    traci.close()

    print("Dynamic simulation finished")


# ==========================================================
# PROGRAM ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    run()