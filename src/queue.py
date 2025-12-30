# Queue data structure for vehicles
# FIFO - First In First Out

class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        # add to back
        self.items.append(item)
    
    def dequeue(self):
        # remove from front
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def front(self):
        # see first item without removing
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def clear(self):
        self.items = []