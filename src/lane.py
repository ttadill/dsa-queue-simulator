from src.queue import Queue

class Lane:
    """
    Represents a traffic lane containing a queue of vehicles
    """

    def __init__(self, name):
        self.name = name
        self.queue = Queue()

    def add_vehicle(self, vehicle):
        self.queue.enqueue(vehicle)

    def process_vehicle(self):
        return self.queue.dequeue()

    def is_empty(self):
        return self.queue.is_empty()
