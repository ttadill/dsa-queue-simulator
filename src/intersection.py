class Intersection:
    def __init__(self, roads: dict):
        """
        roads = {
            "A": [AL1, AL2, AL3],
            "B": [BL1, BL2, BL3],
            ...
        }
        """
        self.roads = roads
        self.priority_lane = roads["A"][1]  # AL2
        self.current_road_index = 0
        self.road_order = ["A", "B", "C", "D"]
        self.priority_mode = False

    def update_lights(self):
        # Priority condition
        if self.priority_lane.queue_size() > 10:
            self.priority_mode = True

        if self.priority_mode:
            self._activate_priority_lane()
            if self.priority_lane.queue_size() < 5:
                self.priority_mode = False
        else:
            self._activate_normal_road()

    def _activate_priority_lane(self):
        for roads in self.roads.values():
            for lane in roads:
                lane.light.state = "RED"
        self.priority_lane.light.state = "GREEN"

    def _activate_normal_road(self):
        active_road = self.road_order[self.current_road_index]

        for road, lanes in self.roads.items():
            for lane in lanes:
                lane.light.state = "GREEN" if road == active_road else "RED"

        self.current_road_index = (self.current_road_index + 1) % 4

    def vehicles_to_serve(self):
        # Assignment formula
        normal_lanes = []
        for road, lanes in self.roads.items():
            for lane in lanes:
                if not lane.is_priority and not lane.is_free:
                    normal_lanes.append(lane)

        total = sum(l.queue_size() for l in normal_lanes)
        if total == 0:
            return 0

        return max(1, total // len(normal_lanes))
