from src.queue import Queue
from src.traffic_light import TrafficLight
from src.vehicle import Vehicle


class Lane:
    def __init__(self, lane_id, queue):
        self.lane_id = lane_id
        self.queue = queue
        self.light = TrafficLight()

    def add_vehicle(self, vehicle: Vehicle):
        if vehicle.priority:
            # Priority vehicle goes to the front
            self.queue.items.insert(0, vehicle)
        else:
            self.queue.enqueue(vehicle)

    def process_vehicle(self):
        if not self.light.is_green():
            return None
        if self.queue.is_empty():
            return None
        return self.queue.dequeue()

    def is_empty(self):
        return self.queue.is_empty()

    def queue_size(self):
        return self.queue.size()
