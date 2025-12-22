class Queue:
    #Queue implementation using FIFO. This queue will store vehicles in traffic lane

    def __init__(self):
        #to store queue items
        self.items = []

    def enqueue(self, item):
        #Add item to the queue
        self.items.append(item)

    def dequeue(self):
        #Remove and return front item
        if self.is_empty():
            return None
        return self.items.pop(0)

    def peek(self):
        #Return the front item without removing it
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        #Check if the queue is empty
        return len(self.items) == 0

    def size(self):
        #Return the number of items in the queue
        return len(self.items)

    def __str__(self):
        return f"Queue({self.items})"
