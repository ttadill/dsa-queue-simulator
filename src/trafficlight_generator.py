import random
import time

lanes = ["laneA.txt", "laneB.txt", "laneC.txt", "laneD.txt"]

while True:
    lane = random.choice(lanes)
    with open(lane, "a") as f:
        f.write("V\n")
    time.sleep(random.randint(1, 3))
