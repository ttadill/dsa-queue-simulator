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

    def update(self, current_green, green_lanes, front_pos=None):
    # Only L2 lanes stop for traffic lights; other lanes move normally
    is_green = (self.road_id in green_lanes and self.lane_id == "L2")

    move_distance = pygame.Vector2(self.speed, 0).rotate(-self.angle)

    # Stop if too close to front vehicle in the same lane
    if front_pos and self.pos.distance_to(front_pos) < 40:
        return

    # Move if lane is green or non-priority
    if is_green or self.lane_id != "L2":
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


class Simulation:
    """Pygame visual simulation for traffic system."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Simulation – Priority Queue with Lights")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28)

        self.roads = ["A", "B", "C", "D"]

        # Create 3 lanes per road
        self.lanes = {}
        for r in self.roads:
            self.lanes[r] = {
                "L1": Lane(f"{r}L1", Queue()),
                "L2": Lane(f"{r}L2", Queue()),  # L2 is priority for A
                "L3": Lane(f"{r}L3", Queue())
            }

        # Mark AL2 as priority
        self.lanes["A"]["L2"].queue_priority = True

        self.intersection = Intersection(self.lanes)

        # Spawn demo vehicles
        vid = 1
        for r in self.roads:
            for lane_id in ["L1","L2","L3"]:
                lane = self.lanes[r][lane_id]
                for _ in range(3):
                    v = Vehicle(vid, priority=(r=="A" and lane_id=="L2"))
                    lane.add_vehicle(v)
                    vid += 1

        # Create visual vehicles
        self.visual_vehicles = {r: {l: [] for l in ["L1","L2","L3"]} for r in self.roads}
        self.sync_visuals_with_lanes()

    def sync_visuals_with_lanes(self):
        for r in self.roads:
            for l in ["L1","L2","L3"]:
                lane_queue = self.lanes[r][l].queue.items
                self.visual_vehicles[r][l] = [
                    VisualVehicle(v, r, l, i) for i, v in enumerate(lane_queue)
                ]

    def draw_roads(self):
        self.screen.fill(BG_GREEN)
        cx, cy = WIDTH//2, HEIGHT//2
        pygame.draw.rect(self.screen, ROAD_COLOR, (cx - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.rect(self.screen, ROAD_COLOR, (0, cy - ROAD_WIDTH//2, WIDTH, ROAD_WIDTH))

    def draw_lights(self):
        cx, cy = WIDTH//2, HEIGHT//2
        positions = {
            "A": (cx, cy - ROAD_WIDTH//2 - 30),
            "B": (cx + ROAD_WIDTH//2 + 30, cy),
            "C": (cx, cy + ROAD_WIDTH//2 + 30),
            "D": (cx - ROAD_WIDTH//2 - 30, cy)
        }
        for r in self.roads:
            light = self.lanes[r]["L2"].light
            color = GREEN if light.is_green() else RED
            pos = positions[r]
            pygame.draw.circle(self.screen, color, pos, LIGHT_RADIUS)

    def draw_queue_info(self):
        y = 20
        for r in self.roads:
            for l in ["L1","L2","L3"]:
                count = self.lanes[r][l].queue_size()
                text = self.font.render(f"{r}-{l} Queue: {count}", True, TEXT_COLOR)
                self.screen.blit(text, (20, y))
                y += 28

    def run(self):
        running = True
        while running:
            self.intersection.update()
            self.draw_roads()
            self.draw_lights()
            self.draw_queue_info()

            # Update visuals
            for r in self.roads:
    for l in ["L1","L2","L3"]:
        lane_queue = self.lanes[r][l].queue.items
        visual_list = self.visual_vehicles[r][l]

        for idx, car in enumerate(visual_list):
            front_pos = visual_list[idx-1].pos if idx>0 else None
            car.update(
                current_green=self.intersection.current_green,
                green_lanes=[self.intersection.current_green],
                front_pos=front_pos
            )
            car.draw(self.screen, is_green=(car.lane_id=="L2" and r==self.intersection.current_green))


                    # Remove vehicles that left screen
                    self.visual_vehicles[r][l] = [
                        v for v in visual_list
                        if -100 < v.pos.x < WIDTH+100 and -100 < v.pos.y < HEIGHT+100
                    ]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Simulation().run()
