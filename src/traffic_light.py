class TrafficLight:
    def __init__(self):
        self.state = "RED"  # RED or GREEN

    def is_green(self):
        return self.state == "GREEN"
