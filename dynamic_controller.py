import traci
import pandas as pd

SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "simulation_map.sumocfg"
SIM_END = 3600

MIN_GREEN = 10
MAIN_CLEAR_THRESHOLD = 5
SIDE_QUEUE_THRESHOLD = 8
SIDE_RELIEF_TIME = 25

def get_lane_queue(lanes):
    return sum(traci.lane.getLastStepHaltingNumber(l) for l in lanes)