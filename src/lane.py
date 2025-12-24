from src.queue import Queue
from src.traffic_light import TrafficLight


class Lane:
    
    def __init__(self, lane_id, queue):
        self.lane_id = lane_id
        self.queue = queue

    def add_vehicle(self, vehicle):
        self.queue.enqueue(vehicle)

    def process_vehicle(self):
        if self.queue.is_empty():
            return None
        return self.queue.dequeue()

    def is_empty(self):
        return self.queue.is_empty()

    def queue_size(self):
        return self.queue.size()
