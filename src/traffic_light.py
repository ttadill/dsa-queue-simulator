# Traffic light state - RED or GREEN

class TrafficLight:
    def __init__(self):
        self.state = "RED"  # start with red
    
    def set_green(self):
        self.state = "GREEN"
    
    def set_red(self):
        self.state = "RED"
    
    def is_green(self):
        return self.state == "GREEN"
    
    def is_red(self):
        return self.state == "RED"