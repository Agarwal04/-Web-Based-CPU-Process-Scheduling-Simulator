from copy import deepcopy

def hrrn(processes):
    processes = deepcopy(processes)  # avoid modifying original list
    n = len(processes)
    current_time = 0
    completed = 0
    scheduled = []

    while completed < n:
        # processes that have arrived and not done yet
        available = [p for p in processes if p.arrival <= current_time and not hasattr(p, "done")]

        if not available:
            current_time += 1
            continue

        # calculate response ratio = (waiting_time + burst) / burst
        for p in available:
            waiting_time = current_time - p.arrival
            p.rr = (waiting_time + p.burst) / p.burst

        # select process with max response ratio
        selected = max(available, key=lambda p: p.rr)

        selected.start = current_time  # ✅ FIXED: Set start time
        selected.waiting = current_time - selected.arrival
        selected.turnaround = selected.waiting + selected.burst
        selected.completion = current_time + selected.burst

        current_time += selected.burst
        setattr(selected, "done", True)

        scheduled.append(selected)
        completed += 1

    return scheduled

 
 
