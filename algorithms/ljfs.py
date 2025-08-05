from copy import deepcopy

def ljfs(processes):
    processes = deepcopy(processes)
    current_time = 0
    completed = 0
    n = len(processes)
    scheduled = []

    while completed < n:
        # processes available at current time and not done yet
        available = [p for p in processes if p.arrival <= current_time and not hasattr(p, "done")]

        if not available:
            current_time += 1
            continue

        # select process with longest burst time
        selected = max(available, key=lambda p: p.burst)

        selected.start = current_time  # ✅ Set start time
        selected.waiting = current_time - selected.arrival
        selected.turnaround = selected.waiting + selected.burst
        selected.completion = current_time + selected.burst

        current_time += selected.burst
        setattr(selected, "done", True)

        scheduled.append(selected)
        completed += 1

    return scheduled
 
 
