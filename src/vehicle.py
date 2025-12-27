class Vehicle:
    def __init__(self, vehicle_id, source_lane):
        self.vehicle_id = vehicle_id
        self.source_lane = source_lane

    def __repr__(self):
        return f"V{self.vehicle_id}"
