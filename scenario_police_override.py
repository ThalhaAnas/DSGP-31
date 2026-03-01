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

    time = 0
    while time < SIM_END:
        traci.simulationStep()
        time += 1

        # Check for Police Override State
        is_override_active = (OVERRIDE_START <= time <= OVERRIDE_END)

        if time == OVERRIDE_START:
            print(f"POLICE OVERRIDE INITIATED at {target_tls}! Forcing Main Road Green.")

        # THE FIX: Continuously lock it to Phase 0 every single step
        if is_override_active:
            traci.trafficlight.setPhase(target_tls, 0)

        elif time == OVERRIDE_END:
            print(f"POLICE OVERRIDE ENDED. Returning {target_tls} to Adaptive AI.")

        # Run normal adaptive logic every LOG_INTERVAL (30s)
        if time % LOG_INTERVAL == 0:
            pressures = {tls: junction_pressure(tls) for tls in tls_ids}
            avg_pressure = sum(pressures.values()) / len(pressures)

            for tls in tls_ids:
                # SKIP adaptive logic for the target TLS if the officer is controlling it
                if tls == target_tls and is_override_active:
                    continue

                logic = traci.trafficlight.getAllProgramLogics(tls)[0]
                greens = [p for p in logic.phases if "G" in p.state]
                if not greens: continue

                main_green = max(greens, key=lambda p: p.duration)
                delta = int(main_green.duration * MAX_ADJUST)

                if pressures[tls] > avg_pressure:
                    main_green.duration += delta
                else:
                    main_green.duration = max(MIN_GREEN, main_green.duration - delta)

                traci.trafficlight.setProgramLogic(tls, logic)

    traci.close()
    print("Scenario finished!")

if __name__ == "__main__":
    run()