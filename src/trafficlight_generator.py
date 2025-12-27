# src/traffic_generator.py
import random

LANES = [
    "AL1", "AL2", "AL3",
    "BL1", "BL2", "BL3",
    "CL1", "CL2", "CL3",
    "DL1", "DL2", "DL3"
]

def generate_traffic(filename="data/vehicles.data", count=100):
    with open(filename, "w") as f:
        for i in range(count):
            lane = random.choice(LANES)
            f.write(f"{i},{lane}\n")

if __name__ == "__main__":
    generate_traffic()
