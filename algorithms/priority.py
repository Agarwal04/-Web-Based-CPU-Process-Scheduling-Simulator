
def priority(processes):
    from copy import deepcopy
    processes = deepcopy(processes)
    n = len(processes)
    completed = 0
    time = 0
    execution_log = []
    
    for p in processes:
        p.remaining = p.burst
    
    last_pid = None
    start_time = 0
    
    while completed < n:
        # Processes arrived and not finished
        available = [p for p in processes if p.arrival <= time and p.remaining > 0]
        if not available:
            time += 1
            continue
        # Select highest priority (lowest priority number)
        current = min(available, key=lambda x: x.priority)
        
        if last_pid != current.pid:
            if last_pid is not None:
                execution_log.append({"pid": last_pid, "start": start_time, "end": time})
            start_time = time
            last_pid = current.pid
        
        current.remaining -= 1
        time += 1
        
        if current.remaining == 0:
            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst
            completed += 1
    
    if last_pid is not None:
        execution_log.append({"pid": last_pid, "start": start_time, "end": time})
    
    return processes, execution_log
 
 
