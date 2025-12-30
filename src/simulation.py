import pygame
import random
import time
from src.queue import Queue
from src.priority_queue import PriorityQueue
from src.vehicle import Vehicle
from src.traffic_light import TrafficLight
from src.traffic_generator import TrafficGenerator

# screen settings
WIDTH = 1400
HEIGHT = 900
FPS = 60

# colors
BG_COLOR = (30, 40, 30)
ROAD_COLOR = (50, 50, 50)
LANE_LINE = (255, 255, 100)
GREEN_LIGHT = (50, 255, 50)
RED_LIGHT = (255, 50, 50)
WHITE = (255, 255, 255)

# car colors
CAR_COLORS = [
    (70, 130, 255),   # blue
    (255, 90, 90),    # red
    (90, 255, 90),    # green
    (255, 200, 70),   # yellow
    (200, 100, 255),  # purple
]

# simulation settings
ROAD_WIDTH = 180
GREEN_TIME = 5.0  # seconds per green light
PRIORITY_HIGH = 10  # AL2 becomes priority when > 10
PRIORITY_LOW = 5   # back to normal when < 5
GEN_INTERVAL = 1.0  # generate vehicle every 1 second


class VisualVehicle:
    # vehicle that shows on screen
    def __init__(self, vehicle, lane, position):
        self.vehicle = vehicle
        self.lane = lane
        self.position = position  # position in queue
        self.color = random.choice(CAR_COLORS)
        self.road = lane[0]  # A, B, C, or D
        self.pos = self.get_wait_pos(position)
        self.target = self.pos.copy()
        self.speed = 3.5
        self.gone = False
        self.passed_intersection = False  # track if car crossed center
    
    def get_wait_pos(self, pos):
        # calculate where car waits in queue
        cx, cy = WIDTH // 2, HEIGHT // 2
        gap = 65
        offset = gap * pos
        
        if self.road == "A":  # top
            return pygame.Vector2(cx - 45, cy - 250 - offset)
        elif self.road == "B":  # right
            return pygame.Vector2(cx + 250 + offset, cy - 45)
        elif self.road == "C":  # bottom
            return pygame.Vector2(cx + 45, cy + 250 + offset)
        else:  # D - left
            return pygame.Vector2(cx - 250 - offset, cy + 45)
    
    def get_exit_pos(self):
        # where car goes when leaving
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        if self.road == "A":
            return pygame.Vector2(cx - 45, HEIGHT + 100)
        elif self.road == "B":
            return pygame.Vector2(-100, cy - 45)
        elif self.road == "C":
            return pygame.Vector2(cx + 45, -100)
        else:
            return pygame.Vector2(WIDTH + 100, cy + 45)
    
    def is_at_intersection(self):
        # check if car is at center
        cx, cy = WIDTH // 2, HEIGHT // 2
        dist = ((self.pos.x - cx) ** 2 + (self.pos.y - cy) ** 2) ** 0.5
        return dist < 100
    
    def update(self, is_green, new_pos):
        # update car position - CONTINUOUS MOVEMENT WHEN GREEN
        self.position = new_pos
        
        if is_green:
            # GREEN LIGHT - ALL CARS MOVE FORWARD CONTINUOUSLY
            if not self.passed_intersection:
                # move towards and through intersection
                self.target = self.get_exit_pos()
                
                # check if passed center
                if self.is_at_intersection():
                    self.passed_intersection = True
            else:
                # already passed, keep moving to exit
                self.target = self.get_exit_pos()
        else:
            # RED LIGHT - WAIT IN QUEUE
            if not self.passed_intersection:
                # stay in waiting position
                self.target = self.get_wait_pos(new_pos)
            else:
                # already through intersection, keep going
                self.target = self.get_exit_pos()
        
        # move towards target
        diff = self.target - self.pos
        dist = diff.length()
        
        if dist > 1:
            diff.normalize_ip()
            self.pos += diff * self.speed
        
        # check if completely off screen
        if (self.pos.x < -150 or self.pos.x > WIDTH + 150 or
            self.pos.y < -150 or self.pos.y > HEIGHT + 150):
            self.gone = True
    
    def draw(self, screen, is_green):
        # draw the car
        w, h = 50, 32
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # brighter when moving, darker when stopped
        if is_green or self.passed_intersection:
            color = self.color
        else:
            color = tuple(max(0, c - 80) for c in self.color)
        
        # car body
        pygame.draw.rect(surf, color, (0, 0, w, h), border_radius=8)
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, w, h), 2, border_radius=8)
        
        # vehicle ID
        font = pygame.font.SysFont("Arial", 14, bold=True)
        text = font.render(str(self.vehicle), True, WHITE)
        rect = text.get_rect(center=(w//2, h//2))
        surf.blit(text, rect)
        
        # rotate based on direction
        angle = {"A": 0, "B": -90, "C": 180, "D": 90}[self.road]
        rotated = pygame.transform.rotate(surf, angle)
        r = rotated.get_rect(center=self.pos)
        screen.blit(rotated, r)


class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Simulation - DSA Assignment")
        self.clock = pygame.time.Clock()
        
        # fonts
        self.font_big = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_med = pygame.font.SysFont("Arial", 24)
        self.font_small = pygame.font.SysFont("Arial", 18)
        
        # lanes with queues
        self.lanes = ["AL2", "BL2", "CL2", "DL2"]
        self.queues = {}
        self.lights = {}
        for lane in self.lanes:
            self.queues[lane] = Queue()
            self.lights[lane] = TrafficLight()
        
        # priority queue for lane order
        self.lane_queue = PriorityQueue()
        for lane in self.lanes:
            self.lane_queue.enqueue(lane, 1)  # all start equal
        
        # state
        self.current_green = "AL2"
        self.priority_mode = False
        self.green_timer = 0
        self.green_duration = GREEN_TIME
        
        # set initial green light
        self.lights["AL2"].set_green()
        
        # generator
        self.generator = TrafficGenerator()
        self.last_gen = time.time()
        
        # visual cars
        self.visual_cars = {lane: [] for lane in self.lanes}
        
        # stats
        self.total_served = 0
        self.stats = {lane: {"served": 0, "wait": 0} for lane in self.lanes}
        self.start_time = time.time()
        self.last_update = time.time()
        
        # track served vehicles per cycle
        self.served_this_cycle = {lane: 0 for lane in self.lanes}
        
        print("\n" + "="*60)
        print("Traffic Simulation Started")
        print("="*60)
        print("GREEN LIGHT = All vehicles move continuously")
        print("RED LIGHT = Vehicles wait in queue")
        print("Press ESC to quit\n")
    
    def generate_vehicle(self):
        # create new vehicle
        vehicle, lane = self.generator.generate_vehicle()
        self.queues[lane].enqueue(vehicle)
        
        # add visual
        pos = self.queues[lane].size() - 1
        visual = VisualVehicle(vehicle, lane, pos)
        self.visual_cars[lane].append(visual)
        
        print(f"Generated {vehicle} in {lane} (Queue: {self.queues[lane].size()})")
    
    def check_priority(self):
        # check if AL2 needs priority
        al2_size = self.queues["AL2"].size()
        
        if al2_size > PRIORITY_HIGH and not self.priority_mode:
            # activate priority
            self.priority_mode = True
            self.lane_queue.update_priority("AL2", 0)  # highest
            print(f"\nPRIORITY MODE ON - AL2 has {al2_size} cars\n")
        
        elif al2_size < PRIORITY_LOW and self.priority_mode:
            # back to normal
            self.priority_mode = False
            self.lane_queue.update_priority("AL2", 1)  # normal
            print(f"\nNORMAL MODE - AL2 has {al2_size} cars\n")
    
    def remove_served_vehicles(self):
        # remove vehicles that passed through intersection
        for lane in self.lanes:
            queue = self.queues[lane]
            visuals = self.visual_cars[lane]
            
            # count how many passed
            passed = 0
            for visual in visuals:
                if visual.passed_intersection and visual.vehicle in queue.items:
                    passed += 1
            
            # remove from queue
            for _ in range(passed):
                if not queue.is_empty():
                    car = queue.dequeue()
                    if car:
                        wait = car.calculate_wait()
                        self.total_served += 1
                        self.stats[lane]["served"] += 1
                        self.stats[lane]["wait"] += wait
                        self.served_this_cycle[lane] += 1
    
    def switch_light(self):
        # report how many served this cycle
        for lane in self.lanes:
            if self.served_this_cycle[lane] > 0:
                print(f"GREEN: {lane} - Served {self.served_this_cycle[lane]} cars")
                self.served_this_cycle[lane] = 0
        
        # change to next lane
        current = self.lane_queue.dequeue()
        
        # put back in queue
        if self.priority_mode and current == "AL2":
            self.lane_queue.enqueue(current, 0)
        else:
            self.lane_queue.enqueue(current, 1)
        
        self.current_green = self.lane_queue.front()
        self.green_timer = 0
        
        # update lights
        for lane in self.lanes:
            if lane == self.current_green:
                self.lights[lane].set_green()
            else:
                self.lights[lane].set_red()
    
    def update(self):
        # main update logic
        now = time.time()
        dt = now - self.last_update
        self.last_update = now
        
        # generate vehicles
        if now - self.last_gen >= GEN_INTERVAL:
            self.generate_vehicle()
            self.last_gen = now
        
        # check priority
        self.check_priority()
        
        # update timer
        self.green_timer += dt
        if self.green_timer >= self.green_duration:
            self.switch_light()
        
        # remove vehicles that passed through
        self.remove_served_vehicles()
        
        # update visual cars - ALL MOVE WHEN GREEN
        for lane in self.lanes:
            items = self.queues[lane].items
            is_green = self.lights[lane].is_green()
            
            for car in self.visual_cars[lane]:
                try:
                    pos = items.index(car.vehicle)
                    car.update(is_green, pos)
                except ValueError:
                    # vehicle already passed, keep moving
                    car.update(is_green, -1)
            
            # remove gone cars
            self.visual_cars[lane] = [c for c in self.visual_cars[lane] if not c.gone]
    
    def draw_roads(self):
        # draw background and roads
        self.screen.fill(BG_COLOR)
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        # vertical road
        pygame.draw.rect(self.screen, ROAD_COLOR, 
                        (cx - ROAD_WIDTH//2, 0, ROAD_WIDTH, HEIGHT))
        # horizontal road
        pygame.draw.rect(self.screen, ROAD_COLOR, 
                        (0, cy - ROAD_WIDTH//2, WIDTH, ROAD_WIDTH))
        
        # lane lines
        for y in range(0, HEIGHT, 35):
            if y < cy - ROAD_WIDTH//2 or y > cy + ROAD_WIDTH//2:
                pygame.draw.line(self.screen, LANE_LINE, 
                               (cx, y), (cx, y + 20), 3)
        
        for x in range(0, WIDTH, 35):
            if x < cx - ROAD_WIDTH//2 or x > cx + ROAD_WIDTH//2:
                pygame.draw.line(self.screen, LANE_LINE, 
                               (x, cy), (x + 20, cy), 3)
    
    def draw_lights(self):
        # draw traffic lights
        cx, cy = WIDTH // 2, HEIGHT // 2
        offset = ROAD_WIDTH // 2 + 50
        
        positions = {
            "AL2": (cx - 70, cy - offset - 30),
            "BL2": (cx + offset + 30, cy - 70),
            "CL2": (cx + 70, cy + offset + 30),
            "DL2": (cx - offset - 30, cy + 70)
        }
        
        for lane, pos in positions.items():
            color = GREEN_LIGHT if self.lights[lane].is_green() else RED_LIGHT
            pygame.draw.circle(self.screen, color, pos, 25)
            pygame.draw.circle(self.screen, (0, 0, 0), pos, 25, 4)
            
            # label
            text = self.font_small.render(lane, True, WHITE)
            rect = text.get_rect(center=(pos[0], pos[1] + 45))
            self.screen.blit(text, rect)
    
    def draw_panel(self):
        # info panel on right
        x, y = WIDTH - 380, 20
        w, h = 360, 520
        
        # background
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((20, 20, 20, 230))
        self.screen.blit(s, (x, y))
        
        x += 20
        y += 20
        
        # title
        text = self.font_big.render("Traffic Control", True, WHITE)
        self.screen.blit(text, (x, y))
        y += 50
        
        # mode
        mode = "PRIORITY MODE" if self.priority_mode else "NORMAL MODE"
        color = (255, 100, 100) if self.priority_mode else (100, 255, 100)
        text = self.font_med.render(mode, True, color)
        self.screen.blit(text, (x, y))
        y += 40
        
        # current green
        text = self.font_med.render(f"Green: {self.current_green}", True, GREEN_LIGHT)
        self.screen.blit(text, (x, y))
        y += 35
        
        # timer
        left = self.green_duration - self.green_timer
        text = self.font_small.render(f"Time: {left:.1f}s", True, WHITE)
        self.screen.blit(text, (x, y))
        y += 40
        
        # queues
        text = self.font_med.render("Queue Sizes:", True, WHITE)
        self.screen.blit(text, (x, y))
        y += 30
        
        for lane in self.lanes:
            size = self.queues[lane].size()
            mark = " *" if lane == "AL2" and self.priority_mode else ""
            light_status = "🟢" if self.lights[lane].is_green() else "🔴"
            text = self.font_small.render(f"{light_status} {lane}: {size}{mark}", True, WHITE)
            self.screen.blit(text, (x + 10, y))
            y += 28
        
        # stats
        y += 15
        text = self.font_med.render("Statistics:", True, WHITE)
        self.screen.blit(text, (x, y))
        y += 30
        
        text = self.font_small.render(f"Total Served: {self.total_served}", True, WHITE)
        self.screen.blit(text, (x + 10, y))
        y += 28
        
        runtime = time.time() - self.start_time
        text = self.font_small.render(f"Runtime: {int(runtime)}s", True, WHITE)
        self.screen.blit(text, (x + 10, y))
        y += 35
        
        # instruction
        text = self.font_small.render("GREEN = All cars move", True, (150, 255, 150))
        self.screen.blit(text, (x, y))
        y += 25
        text = self.font_small.render("RED = Cars wait", True, (255, 150, 150))
        self.screen.blit(text, (x, y))
    
    def draw_cars(self):
        # draw all vehicles
        for lane in self.lanes:
            is_green = self.lights[lane].is_green()
            for car in self.visual_cars[lane]:
                car.draw(self.screen, is_green)
    
    def run(self):
        # main loop
        running = True
        
        while running:
            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # update
            self.update()
            
            # draw
            self.draw_roads()
            self.draw_lights()
            self.draw_cars()
            self.draw_panel()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        self.print_stats()
    
    def print_stats(self):
        # final stats
        print("\n" + "="*60)
        print("Final Statistics")
        print("="*60)
        print(f"Total Served: {self.total_served}")
        print(f"Runtime: {int(time.time() - self.start_time)}s\n")
        
        for lane in self.lanes:
            served = self.stats[lane]["served"]
            total_wait = self.stats[lane]["wait"]
            avg = total_wait / served if served > 0 else 0
            print(f"{lane}: {served} served, avg wait {avg:.2f}s")
        
        print("="*60 + "\n")