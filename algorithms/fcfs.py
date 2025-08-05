def fcfs(processes):
    processes.sort(key=lambda p: p.arrival)
    current_time = 0
    execution_log = []

    for process in processes:
        if current_time < process.arrival:
            current_time = process.arrival
        process.start = current_time
        start_time = current_time
        current_time += process.burst
        end_time = current_time

        process.completion = current_time
        process.turnaround = process.completion - process.arrival
        process.waiting = process.turnaround - process.burst

        execution_log.append({'pid': process.pid, 'start': start_time, 'end': end_time})

    return processes, execution_log
 
 
