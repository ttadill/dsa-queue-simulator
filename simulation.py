# simulation.py
import pygame
import random
from src.queue import Queue
from src.lane import Lane
from src.vehicle import Vehicle
from src.intersection import Intersection

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1000, 800
FPS = 60
LANE_WIDTH = 50
ROAD_WIDTH = LANE_WIDTH * 3

BG_GREEN = (24, 45, 24)
ROAD_COLOR = (33, 33, 33)
TEXT_COLOR = (200, 200, 200)


class VisualVehicle:
    """Wraps your existing Vehicle for Pygame visuals."""
    def __init__(self, vehicle, road_id, index_in_queue):
        self.vehicle = vehicle
        self.road_id = road_id
        self.index_in_queue = index_in_queue
        self.speed = random.uniform(2, 3)
        self.color = random.choice([
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
        move_distance = pygame.Vector2(self.speed, 0).rotate(-self.angle)
        if front_pos and self.pos.distance_to(front_pos) < 50:
            return
        if is_green:
            self.pos += move_distance

    def draw(self, surf, is_green):
        rect = pygame.Rect(0, 0, 40, 24)
        rect.center = self.pos
        color = self.color if is_green else (180, 180, 180)
        pygame.draw.rect(surf, color, rect, border_radius=5)


class Simulation:
    """Pygame visual simulation for your traffic system."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Simulation – Visual Queue")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28)

        # Roads and green light control
        self.roads = ["A", "B", "C", "D"]
        self.green_timer = 0
        self.green_duration = 200  # frames (~3s)
        self.current_green = "A"

        # Create queues and lanes
        self.queues = {r: Queue() for r in self.roads}
        self.lanes = {r: Lane(r, self.queues[r]) for r in self.roads}

        # Initialize Intersection with lanes
        self.intersection = Intersection(self.lanes)

        # Spawn some demo vehicles in each lane
        vid = 1
        for road in self.roads:
            for _ in range(3):
                v = Vehicle(vid)
                self.lanes[road].add_vehicle(v)
                vid += 1

        # Create visual wrappers
        self.visual_vehicles = {r: [] for r in self.roads}
        self.sync_visuals_with_lanes()

    def sync_visuals_with_lanes(self):
        """Wrap vehicles in visual objects based on lane queues."""
        for road in self.roads:
            lane_queue = self.lanes[road].queue.items
            self.visual_vehicles[road] = [
                VisualVehicle(v, road, i) for i, v in enumerate(lane_queue)
            ]

    def draw_roads(self):
        self.screen.fill(BG_GREEN)
        cx, cy = WIDTH // 2, HEIGHT // 2
        # vertical
        pygame.draw.rect(self.screen, ROAD_COLOR, (cx - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT))
        # horizontal
        pygame.draw.rect(self.screen, ROAD_COLOR, (0, cy - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH))

    def draw_queue_info(self):
        y = 20
        for road in self.roads:
            count = self.lanes[road].queue_size()
            text = self.font.render(f"Lane {road} Queue: {count}", True, TEXT_COLOR)
            self.screen.blit(text, (20, y))
            y += 35

    def update_green_light(self):
        self.green_timer += 1
        if self.green_timer > self.green_duration:
            self.green_timer = 0
            idx = self.roads.index(self.current_green)
            self.current_green = self.roads[(idx + 1) % len(self.roads)]

    def process_lanes(self):
        """Process one vehicle per lane each step (like your old text simulation)."""
        for lane in self.lanes.values():
            lane.process_vehicle()  # assumes Lane has a process_vehicle() method

    def run(self):
        running = True
        while running:
            self.update_green_light()
            self.draw_roads()
            self.draw_queue_info()

            # Process vehicles in lanes
            self.process_lanes()

            # Update visuals
            for road in self.roads:
                lane_queue = self.lanes[road].queue.items
                visual_list = self.visual_vehicles[road]

                for idx, car in enumerate(visual_list):
                    is_green = (road == self.current_green)
                    front_pos = visual_list[idx - 1].pos if idx > 0 else None
                    car.update(is_green, front_pos)
                    car.draw(self.screen, is_green)

                # Remove vehicles that exited screen
                self.visual_vehicles[road] = [
                    v for v in visual_list
                    if -100 < v.pos.x < WIDTH + 100 and -100 < v.pos.y < HEIGHT + 100
                ]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(FPS)
