class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.priority = priority
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0
        self.start = None  # First time process gets CPU
 
 
