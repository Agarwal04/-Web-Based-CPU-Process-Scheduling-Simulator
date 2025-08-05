def calculate_averages(processes):
    n = len(processes)
    avg_waiting = sum(p.waiting for p in processes) / n
    avg_turnaround = sum(p.turnaround for p in processes) / n
    return avg_waiting, avg_turnaround 
