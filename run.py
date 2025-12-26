from src.queue import Queue
from src.lane import Lane
from src.vehicle import Vehicle
from src.metrics import Metrics
from src.intersection import Intersection
import time


def print_status(lanes, step):
    print(f"\n--- Step {step} ---")
    for lane in lanes:
        vehicles = [v.vehicle_id for v in lane.queue.items]
        print(f"Lane ID: {lane.lane_id}")
        print(f"Queue size: {lane.queue_size()}")
        print(f"Vehicles in queue: {vehicles}")
        print("-" * 30)


def run_simulation():
    print("Starting traffic simulation (Day 4 / Day 5)\n")

    # Create queues
    queue_a = Queue()
    queue_b = Queue()

    # Create lanes
    lane_a = Lane("Lane-A", queue_a)
    lane_b = Lane("Lane-B", queue_b)

    lanes = [lane_a, lane_b]

    # Add vehicles
    lane_a.add_vehicle(Vehicle(1))
    lane_a.add_vehicle(Vehicle(2))
    lane_b.add_vehicle(Vehicle(3))
    lane_b.add_vehicle(Vehicle(4))

    step = 0
    current_lane = 0
    metrics = Metrics()

    while not all(lane.is_empty() for lane in lanes):
        step += 1
        print_status(lanes, step)

        lane = lanes[current_lane]
        processed = lane.process_vehicle()

        if processed:
            metrics.record_vehicle()
            print(f"Processed vehicle from {lane.lane_id}: {processed}")
        else:
            print(f"No vehicle processed from {lane.lane_id}")

        # Move to next lane (round-robin)
        current_lane = (current_lane + 1) % len(lanes)

        time.sleep(1)

    print("\nSimulation complete.")
    metrics.print_summary()


if __name__ == "__main__":
    run_simulation()
