# simulation.py
import pygame
import random
from src.queue import Queue
from src.lane import Lane
from src.vehicle import Vehicle

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1000, 800
FPS = 60
LANE_WIDTH = 50
ROAD_WIDTH = LANE_WIDTH * 3
T_PER_VEHICLE = 50  # frames per vehicle for green light

BG_GREEN = (24, 45, 24)
ROAD_COLOR = (33, 33, 33)
TEXT_COLOR = (200, 200, 200)
PRIORITY_COLOR = (255, 0, 0)
LIGHT_RADIUS = 15
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class TrafficLight:
    """Manages light state for a lane."""
    def __init__(self, green_duration=200, red_duration=200):
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.timer = 0
        self.state = "RED"

    def update(self):
        self.timer += 1
        if self.state == "GREEN" and self.timer >= self.green_duration:
            self.state = "RED"
            self.timer = 0
        elif self.state == "RED" and self.timer >= self.red_duration:
            self.state = "GREEN"
            self.timer = 0

    def is_green(self):
        return self.state == "GREEN"


class VisualVehicle:
    """Wraps your Vehicle for Pygame visuals."""
    def __init__(self, vehicle, road_id, lane_id, index_in_queue):
        self.vehicle = vehicle
        self.road_id = road_id
        self.lane_id = lane_id
        self.index_in_queue = index_in_queue
        self.speed = random.uniform(2, 3)
        self.color = PRIORITY_COLOR if vehicle.priority else random.choice([
            (60, 120, 255),
            (255, 80, 80),
            (220, 220, 220),
            (180, 100, 255)
        ])
        self.pos = self.spawn_position()
        self.angle = self.spawn_angle()

    def spawn_position(self):
        cx, cy = WIDTH // 2, HEIGHT // 2
        offset = 60 * self.index_in_queue
        if self.road_id == "A":
            return pygame.Vector2(cx, -40 - offset)
        if self.road_id == "B":
            return pygame.Vector2(WIDTH + 40 + offset, cy)
        if self.road_id == "C":
            return pygame.Vector2(cx, HEIGHT + 40 + offset)
        return pygame.Vector2(-40 - offset, cy)

    def spawn_angle(self):
        return {"A": 270, "B": 180, "C": 90, "D": 0}[self.road_id]

    def update(self, is_green, front_pos=None):
        """Move the vehicle if the light is green and there’s space ahead."""
        move_distance = pygame.Vector2(self.speed, 0).rotate(-self.angle)

        # Stop if too close to the vehicle in front
        if front_pos and self.pos.distance_to(front_pos) < 50:
            return

        # Move only if green light
        if is_green:
            self.pos += move_distance

    def draw(self, surf, is_green):
        rect = pygame.Rect(0, 0, 40, 24)
        rect.center = self.pos
        color = self.color if is_green else (180, 180, 180)
        pygame.draw.rect(surf, color, rect, border_radius=5)



class Intersection:
    """Manages lane order, lights, and priority logic."""
    def __init__(self, lanes):
        self.lanes = lanes
        self.road_order = ["A", "B", "C", "D"]
        self.current_idx = 0
        self.current_green = "A"
        self.green_timer = 0
        self.green_duration = T_PER_VEHICLE
        # Attach traffic lights to L2 lanes (priority lanes)
        for r in self.road_order:
            self.lanes[r]["L2"].light = TrafficLight(self.green_duration, self.green_duration)

    def update(self):
    # Priority check for AL2
    priority_lane = self.lanes["A"]["L2"]
    if priority_lane.queue_size() > 10:
        self.current_green = "A"
        self.green_duration = max(priority_lane.queue_size() * 20, 50)
    else:
        # Normal round-robin
        self.green_timer += 1
        if self.green_timer > self.green_duration:
            self.green_timer = 0
            self.current_idx = (self.current_idx + 1) % len(self.road_order)
            self.current_green = self.road_order[self.current_idx]
            lane = self.lanes[self.current_green]["L2"]
            self.green_duration = max(lane.queue_size() * 20, 50)

    # Process vehicles in all lanes (not just current green)
    for r in self.roads:
        for l in ["L1","L2","L3"]:
            self.lanes[r][l].process_vehicle()


        # Set other lanes' lights to red
        for r in self.road_order:
            for l in ["L2"]:
                if r != self.current_green:
                    self.lanes[r][l].light.state = "RED"

        # Process vehicle in current green lane
        self.lanes[self.current_green]["L2"].process_vehicle()


def run(self):
    running = True
    while running:
        # Update intersection logic
        self.intersection.update()

        # Draw roads and queue info
        self.draw_roads()
        self.draw_queue_info()

        # Update vehicle visuals
        for r in self.roads:
            for l in ["L1", "L2", "L3"]:
                visual_list = self.visual_vehicles[r][l]

                for idx, car in enumerate(visual_list):
                    is_green = (r == self.intersection.current_green and l == "L2")
                    front_pos = visual_list[idx-1].pos if idx > 0 else None
                    car.update(is_green, front_pos)
                    car.draw(self.screen, is_green)

                # Remove vehicles that left the screen
                self.visual_vehicles[r][l] = [
                    v for v in visual_list
                    if -100 < v.pos.x < WIDTH + 100 and -100 < v.pos.y < HEIGHT + 100
                ]

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        self.clock.tick(FPS)



if __name__ == "__main__":
    Simulation().run()
