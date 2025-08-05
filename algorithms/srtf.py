def srtf(processes):
    from copy import deepcopy
    processes = deepcopy(processes)
    n = len(processes)
    completed = 0
    time = 0
    execution_log = []
    
    # Initialize remaining times
    for p in processes:
        p.remaining = p.burst
    
    last_pid = None
    start_time = 0
    
    while completed < n:
        # Find process with shortest remaining time available at 'time'
        available = [p for p in processes if p.arrival <= time and p.remaining > 0]
        if not available:
            time += 1
            continue
        current = min(available, key=lambda x: x.remaining)
        
        # Run for 1 unit of time (preemptive)
        if last_pid != current.pid:
            # If switching process, log the previous one
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
    
    # Log the last running process interval
    if last_pid is not None:
        execution_log.append({"pid": last_pid, "start": start_time, "end": time})
    
    return processes, execution_log
 
 
