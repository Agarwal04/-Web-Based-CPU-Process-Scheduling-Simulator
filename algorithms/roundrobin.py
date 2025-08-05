from collections import deque
from copy import deepcopy

def round_robin(processes, time_quantum):
    proc_map = {p.pid: p for p in processes}  # Map for syncing updates
    processes = deepcopy(processes)
    
    for p in processes:
        p.remaining = p.burst
        p.start = None

    processes.sort(key=lambda p: p.arrival)
    queue = deque()
    time = 0
    i = 0
    completed = 0
    n = len(processes)
    execution_log = []

    while completed < n:
        while i < n and processes[i].arrival <= time:
            queue.append(processes[i])
            i += 1

        if queue:
            current = queue.popleft()
            exec_time = min(time_quantum, current.remaining)

            if current.start is None:
                current.start = time  # Record first start time (optional)

            start_time = time
            time += exec_time
            current.remaining -= exec_time
            execution_log.append({
                "pid": current.pid,
                "start": start_time,
                "end": time
            })

            while i < n and processes[i].arrival <= time:
                queue.append(processes[i])
                i += 1

            if current.remaining == 0:
                current.completion = time
                current.turnaround = current.completion - current.arrival
                current.waiting = current.turnaround - current.burst
                completed += 1
                # Update original object too
                orig = proc_map[current.pid]
                orig.completion = current.completion
                orig.turnaround = current.turnaround
                orig.waiting = current.waiting
                orig.start = current.start
            else:
                queue.append(current)
        else:
            time += 1

    # Return original list (now updated), and execution log for Gantt chart
    return list(proc_map.values()), execution_log
 
 
