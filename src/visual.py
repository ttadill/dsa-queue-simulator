import pygame
import random
import math

from src.intersection import Intersection
from src.vehicle import Vehicle

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1000, 800
FPS = 60

LANE_WIDTH = 50
ROAD_WIDTH = LANE_WIDTH * 3

BG_GREEN = (24, 45, 24)
ROAD_COLOR = (33, 33, 33)
CENTER_LINE = (255, 214, 0)

GLOW_RED = (255, 50, 50)
GLOW_GREEN = (50, 255, 150)

TEXT_COLOR = (200, 200, 200)


class VisualVehicle:
    """
    Visual wrapper around your existing Vehicle object.
    """

    def __init__(self, vehicle, road_id):
        self.vehicle = vehicle
        self.road_id = road_id
        self.speed = random.uniform(1.5, 3)
        self.pos = self.spawn_position()
        self.angle = self.spawn_angle()

        self.color = random.choice([
            (60, 120, 255),
            (255, 80, 80),
            (220, 220, 220),
            (180, 100, 255)
        ])

    def spawn_position(self):
        cx, cy = WIDTH // 2, HEIGHT // 2
        if self.road_id == "A":
            return pygame.Vector2(cx, -40)
        if self.road_id == "B":
            return pygame.Vector2(WIDTH + 40, cy)
        if self.road_id == "C":
            return pygame.Vector2(cx, HEIGHT + 40)
        return pygame.Vector2(-40, cy)

    def spawn_angle(self):
        return {"A": 270, "B": 180, "C": 90, "D": 0}[self.road_id]

    def update(self, is_green):
        if not is_green:
            return

        move = pygame.Vector2(self.speed, 0).rotate(-self.angle)
        self.pos += move

    def draw(self, surf):
        rect = pygame.Rect(0, 0, 40, 24)
        rect.center = self.pos
        pygame.draw.rect(surf, self.color, rect, border_radius=5)


class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Simulation – Day 5")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Outfit", 28)

        self.intersection = Intersection()

        self.visual_vehicles = {
            "A": [],
            "B": [],
            "C": [],
            "D": []
        }

        self.spawn_demo_vehicles()

    def spawn_demo_vehicles(self):
        vid = 1
        for road in ["A", "B", "C", "D"]:
            lane = self.intersection.lanes[road]
            for _ in range(3):
                v = Vehicle(vid)
                lane.add_vehicle(v)
                self.visual_vehicles[road].append(
                    VisualVehicle(v, road)
                )
                vid += 1

    def draw_roads(self):
        self.screen.fill(BG_GREEN)
        cx, cy = WIDTH // 2, HEIGHT // 2

        pygame.draw.rect(
            self.screen, ROAD_COLOR,
            (cx - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT)
        )
        pygame.draw.rect(
            self.screen, ROAD_COLOR,
            (0, cy - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH)
        )

    def run(self):
        while True:
            self.intersection.update()

            self.draw_roads()

            green = self.intersection.current_green

            for road, vehicles in self.visual_vehicles.items():
                is_green = (road == green)
                for car in vehicles:
                    car.update(is_green)
                    car.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Simulation().run()
