# Priority queue for managing which lane gets green light
# Lower number = higher priority

class PriorityItem:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority

class PriorityQueue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, data, priority):
        # add item with priority
        item = PriorityItem(data, priority)
        
        if len(self.items) == 0:
            self.items.append(item)
        else:
            # find correct position based on priority
            added = False
            for i in range(len(self.items)):
                if priority < self.items[i].priority:
                    self.items.insert(i, item)
                    added = True
                    break
            
            if not added:
                self.items.append(item)
    
    def dequeue(self):
        # remove highest priority item
        if len(self.items) > 0:
            return self.items.pop(0).data
        return None
    
    def front(self):
        # see highest priority without removing
        if len(self.items) > 0:
            return self.items[0].data
        return None
    
    def update_priority(self, data, new_priority):
        # change priority of existing item
        # first remove it
        for i in range(len(self.items)):
            if self.items[i].data == data:
                self.items.pop(i)
                break
        # then add again with new priority
        self.enqueue(data, new_priority)
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)