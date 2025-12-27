from src.queue import Queue
from src.traffic_light import TrafficLight

class Lane:
    def __init__(self, lane_id, is_priority=False, is_free=False):
        self.lane_id = lane_id
        self.queue = Queue()
        self.light = TrafficLight()
        self.is_priority = is_priority
        self.is_free = is_free  # left-turn lane

    def add_vehicle(self, vehicle):
        self.queue.enqueue(vehicle)

    def serve_vehicle(self):
        if self.light.is_green() and not self.queue.is_empty():
            return self.queue.dequeue()
        return None

    def queue_size(self):
        return self.queue.size()
