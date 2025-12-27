# simulation.py

import time
from queue_ds import Queue

T_PER_VEHICLE = 2   # time for one vehicle


class Simulation:
    def __init__(self):
        # Queues for L2 lanes
        self.lanes = {
            "A": Queue(),   # AL2 = priority lane
            "B": Queue(),
            "C": Queue(),
            "D": Queue()
        }

        self.road_order = ["A", "B", "C", "D"]
        self.current_index = 0
        self.current_green = "A"
        self.priority_active = False

        # Sample vehicles (for testing)
        for _ in range(8):
            self.lanes["B"].queue.append("V")
            self.lanes["C"].queue.append("V")
            self.lanes["D"].queue.append("V")

    def update(self):
        priority_lane = self.lanes["A"]

        # Rule: if AL2 > 10 → priority
        if priority_lane.size() > 10:
            self.priority_active = True

        # Priority stays until < 5
        if self.priority_active:
            self.current_green = "A"
            vehicles = priority_lane.size()

            if priority_lane.size() < 5:
                self.priority_active = False

        else:
            # Normal round robin
            self.current_index = (self.current_index + 1) % 4
            self.current_green = self.road_order[self.current_index]

            # Average formula (BL2, CL2, DL2)
            total = (
                self.lanes["B"].size() +
                self.lanes["C"].size() +
                self.lanes["D"].size()
            )
            vehicles = max(1, total // 3)

        self.serve_vehicles(self.current_green, vehicles)

    def serve_vehicles(self, road, count):
        print(f"GREEN: {road} | Serving {count} vehicles")

        for _ in range(count):
            if self.lanes[road].size() > 0:
                self.lanes[road].queue.pop(0)

        time.sleep(count * T_PER_VEHICLE)

    def run(self):
        print("DSA Queue Traffic Simulation Started")
        while True:
            self.update()
