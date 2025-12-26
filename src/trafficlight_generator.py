import random
import time
import os

# L2 lanes only (matches visual_simulation.py)
LANES = ["AL2", "BL2", "CL2", "DL2"]

DATA_DIR = "lane_data"


def ensure_lane_files():
    """
    Ensure lane_data directory and lane files exist.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for lane in LANES:
        path = os.path.join(DATA_DIR, f"{lane}.txt")
        if not os.path.exists(path):
            open(path, "w").close()


def generate_vehicles():
    """
    Randomly generate vehicles and append IDs to lane files.
    """
    ensure_lane_files()

    for lane in LANES:
        path = os.path.join(DATA_DIR, f"{lane}.txt")

        vehicles_to_add = 0

        # 80% chance at least one vehicle
        if random.random() < 0.8:
            vehicles_to_add += 1

        # 40% chance of a second vehicle
        if random.random() < 0.4:
            vehicles_to_add += 1

        if vehicles_to_add == 0:
            continue

        with open(path, "a") as f:
            for _ in range(vehicles_to_add):
                vehicle_id = f"{lane}_{int(time.time() * 1000)}"
                f.write(vehicle_id + "\n")

        print(f"[GENERATOR] Added {vehicles_to_add} vehicle(s) to {lane}")


def run_generator():
    print("Traffic generator running (Ctrl+C to stop)")
    try:
        while True:
            generate_vehicles()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nTraffic generator stopped.")


if __name__ == "__main__":
    run_generator()
