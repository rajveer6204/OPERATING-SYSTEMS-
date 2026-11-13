from collections import deque

processes = [
    ["P1", 0, 5],
    ["P2", 1, 4],
    ["P3", 2, 2],
    ["P4", 8, 3]
]

quantum = 2

remaining = {p[0]: p[2] for p in processes}
completion = {}
first_response = {}
gantt = []

ready = deque()
time = 0
i = 0

while i < len(processes) or ready:

    # Add arrived processes
    while i < len(processes) and processes[i][1] <= time:
        ready.append(processes[i][0])
        i += 1

    # CPU idle
    if not ready:
        if i < len(processes):
            gantt.append(("IDLE", time, processes[i][1]))
            time = processes[i][1]
            continue

    p = ready.popleft()

    # Response time: first time process gets CPU
    if p not in first_response:
        first_response[p] = time

    start = time
    run_time = min(quantum, remaining[p])

    time += run_time
    remaining[p] -= run_time

    gantt.append((p, start, time))

    # Add processes that arrived during execution
    while i < len(processes) and processes[i][1] <= time:
        ready.append(processes[i][0])
        i += 1

    if remaining[p] > 0:
        ready.append(p)
    else:
        completion[p] = time


# Calculate metrics
print("\nPROCESS SCHEDULING RESULTS")
print("-" * 55)
print(f"{'Process':<10}{'CT':<10}{'TAT':<10}{'WT':<10}{'RT':<10}")

total_tat = total_wt = total_rt = 0

for p, at, bt in processes:
    ct = completion[p]
    tat = ct - at
    wt = tat - bt
    rt = first_response[p] - at

    total_tat += tat
    total_wt += wt
    total_rt += rt

    print(f"{p:<10}{ct:<10}{tat:<10}{wt:<10}{rt:<10}")

n = len(processes)

print("-" * 55)
print("Average Turnaround Time =", total_tat / n)
print("Average Waiting Time    =", total_wt / n)
print("Average Response Time   =", total_rt / n)


# Gantt Chart
print("\nGANTT CHART")
print("-" * 60)

for process, start, end in gantt:
    print(f"| {process} ", end="")

print("|")

for process, start, end in gantt:
    print(f"{start:<6}", end="")

print(end)