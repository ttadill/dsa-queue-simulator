class Intersection:
    def __init__(self, lanes: dict):
        self.lanes = lanes
        self.normal_lanes = [l for l in lanes.values() if not l.is_priority]
        self.priority_lane = next((l for l in lanes.values() if l.is_priority), None)
        self.current_index = 0

    def update(self):
        # Serve priority lane if >10 vehicles
        if self.priority_lane and self.priority_lane.queue_size() > 10:
            self._set_green(self.priority_lane)
        else:
            lane = self.normal_lanes[self.current_index]
            self._set_green(lane)
            self.current_index = (self.current_index + 1) % len(self.normal_lanes)

    def _set_green(self, active_lane):
        for lane in self.lanes.values():
            lane.light.state = "GREEN" if lane == active_lane else "RED"
