import time


class StopWatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_elapsed_time = 0

    def start(self):
        self.start_time = time.time()
        self.end_time = self.start_time

    def reset(self):
        self.start_time = None
        self.total_elapsed_time = 0

    def elapsed(self):
        if self.start_time == self.end_time:
            return self.total_elapsed_time + time.time() - self.start_time

        return self.total_elapsed_time

    def stop(self):
        if self.start_time is None:
            return 0
        self.end_time = time.time()
        self.total_elapsed_time += self.end_time - self.start_time
        return self.total_elapsed_time
