"""
Main runner file to check project progress.
This file will evolve as more components are added.
"""

from src.lane import Lane
from src.vehicle import Vehicle
import time


def print_status(lane, step):
    print(f"\n--- Step {step} ---")
    vehicles = [v.vehicle_id for v in lane.queue.items]
    print(f"Lane: {lane.lane_id}")
    print(f"Queue size: {lane.size()}")
    print(f"Vehicles: {vehicles}")
    print("-" * 30)


def run_simulation():
    print("Starting basic traffic simulation (Day 2)\n")

    # Create a lane
    lane = Lane("Lane-A")

    # Add some vehicles initially
    lane.add_vehicle(Vehicle(1))
    lane.add_vehicle(Vehicle(2))
    lane.add_vehicle(Vehicle(3))

    step = 0

    while not lane.is_empty():
        step += 1
        print_status(lane, step)

        processed = lane.process_vehicle()
        print(f"Processed vehicle: {processed}")

        time.sleep(1)

    print("\nSimulation complete. Lane is empty.")


if __name__ == "__main__":
    run_simulation()
