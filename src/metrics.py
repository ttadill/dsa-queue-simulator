class Metrics:
    def __init__(self):
        self.total_processed = 0

    def record(self):
        self.total_processed += 1

    def summary(self):
        print(f"Total vehicles processed: {self.total_processed}")
