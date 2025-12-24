class TrafficLight:
    def __init__(self, green_duration=3, red_duration=3):
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.timer = 0
        self.state = "RED"

    def update(self):
        self.timer += 1

        if self.state == "RED" and self.timer >= self.red_duration:
            self.state = "GREEN"
            self.timer = 0

        elif self.state == "GREEN" and self.timer >= self.green_duration:
            self.state = "RED"
            self.timer = 0

    def is_green(self):
        return self.state == "GREEN"

    def __str__(self):
        return f"TrafficLight({self.state})"
