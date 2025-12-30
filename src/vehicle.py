# Vehicle class to store vehicle data

import time

class Vehicle:
    # counter for unique IDs
    id_counter = 0
    
    def __init__(self, lane):
        Vehicle.id_counter += 1
        self.id = Vehicle.id_counter
        self.lane = lane  # which lane (AL2, BL2, etc)
        self.arrival_time = time.time()
        self.wait_time = 0
    
    def calculate_wait(self):
        # how long vehicle has been waiting
        self.wait_time = time.time() - self.arrival_time
        return self.wait_time
    
    def __str__(self):
        return f"V{self.id}"