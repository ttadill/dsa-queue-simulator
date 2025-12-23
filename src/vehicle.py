class Vehicle:
    """
    Represents a vehicle arriving at the traffic junction
    """

    def __init__(self, vehicle_id, priority=False):
        self.vehicle_id = vehicle_id
        self.priority = priority

    def __str__(self):
        return f"Vehicle({self.vehicle_id}, priority={self.priority})"

