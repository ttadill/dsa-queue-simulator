# Generates vehicles automatically

import random
import time
from src.vehicle import Vehicle

class TrafficGenerator:
    def __init__(self):
        self.lanes = ["AL2", "BL2", "CL2", "DL2"]
        self.running = False
    
    def generate_vehicle(self):
        # pick random lane (35% chance for AL2 to trigger priority)
        if random.random() < 0.35:
            lane = "AL2"
        else:
            lane = random.choice(["BL2", "CL2", "DL2"])
        
        vehicle = Vehicle(lane)
        return vehicle, lane
    
    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False