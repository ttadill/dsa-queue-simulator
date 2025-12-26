
class LanePriorityQueue:
    """
    Simplified priority queue.
    Only L2 road of lane A is ever treated as priority. Other lanes are never promoted to priority unlike in previous iterations. This keeps the traffic logic aligned with the scope of the assignment.
    """

    def __init__(self, priority_lane_id = "AL2"):
        self.priority_lane_id = priority_lane_id
        self.priority_lane = None

    def register_lane(self, lane):
        if lane.lane_id == self.priority_lane_id:
            self.priority_lane = lane

    def peek(self):
        if self.priority_lane and self.priority_lane.size()>0:
            return self.priority_lane
        return None
    
    def dequeue(self):
        return self.peek()

    def is_empty(self):
        return self.peek() is None
    
    def __str__(self):
        if self.priority_lane:
            return f"[PRIORITY: {self.priority_lane.lane_id}]"
        return "[NO PRIORITY LANE]"