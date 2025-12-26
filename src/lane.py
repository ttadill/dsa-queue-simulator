from src.queue import Queue
from src.vehicle import Vehicle
from src.traffic_light import TrafficLight

class Lane:
    def __init__(self, lane_id, is_priority=False):
        self.lane_id = lane_id
        self.queue = Queue()
        self.light = TrafficLight()
        self.is_priority = is_priority

    def add_vehicle(self, vehicle: Vehicle):
        if self.is_priority and vehicle.priority:
            self.queue.items.insert(0, vehicle)
        else:
            self.queue.enqueue(vehicle)

    def process_vehicle(self):
        if not self.light.is_green():
            return None
        if self.queue.is_empty():
            return None
        return self.queue.dequeue()

    def queue_size(self):
        return self.queue.size()
