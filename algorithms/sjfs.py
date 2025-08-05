def sjfs(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    is_completed = [False] * n

    while completed != n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if processes[i].arrival <= current_time and not is_completed[i]:
                if processes[i].burst < min_burst:
                    min_burst = processes[i].burst
                    idx = i
                elif processes[i].burst == min_burst:
                    if processes[i].arrival < processes[idx].arrival:
                        idx = i

        if idx != -1:
            processes[idx].start = current_time  # ✅ Set start time
            current_time += processes[idx].burst
            processes[idx].completion = current_time
            processes[idx].turnaround = processes[idx].completion - processes[idx].arrival
            processes[idx].waiting = processes[idx].turnaround - processes[idx].burst
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1  # CPU is idle

    return processes
 
 
