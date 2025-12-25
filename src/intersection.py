class Intersection:
    def __init__(self, lanes):
        self.lanes = lanes
        self.current_index = 0

    def step(self):
        lane = self.lanes[self.current_index]
        vehicle = lane.process_vehicle()

        # move to next lane
        self.current_index = (self.current_index + 1) % len(self.lanes)
        return vehicle
