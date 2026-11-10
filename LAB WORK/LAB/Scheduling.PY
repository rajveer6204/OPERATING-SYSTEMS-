
def get_processes():
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        print(f"\nProcess P{i + 1}")
        pid = input("Process ID: ")
        at = int(input("Arrival Time: "))
        bt = int(input("Burst Time: "))
        priority = int(input("Priority (smaller number = higher priority): "))

        if at < 0 or bt <= 0 or priority < 0:
            raise ValueError("Invalid input: AT >= 0, BT > 0, Priority >= 0")

        processes.append({
            "pid": pid, "at": at, "bt": bt,
            "priority": priority
        })

    if len({p["pid"] for p in processes}) != n:
        raise ValueError("Process IDs must be unique.")

    return processes


def priority_scheduling(processes):
    print("\n--- Non-Preemptive Priority Scheduling ---")
    print("Convention: Smaller priority number = Higher priority")

    remaining = processes.copy()
    time = 0
    gantt = []
    results = {}

    while remaining:
        available = [p for p in remaining if p["at"] <= time]

        if not available:
            next_at = min(p["at"] for p in remaining)
            gantt.append(("IDLE", time, next_at))
            time = next_at
            continue

        # Priority first, then arrival time, then input order
        p = min(available, key=lambda x: (x["priority"], x["at"]))
        start = time
        time += p["bt"]
        ct = time

        results[p["pid"]] = {
            "ct": ct,
            "tat": ct - p["at"],
            "wt": ct - p["at"] - p["bt"]
        }

        gantt.append((p["pid"], start, time))
        remaining.remove(p)

    print("Execution sequence:")
    for pid, start, end in gantt:
        print(f"| {pid} ({start}-{end}) ", end="")
    print("|")

    print("\nPID\tCT\tTAT\tWT")
    for p in processes:
        r = results[p["pid"]]
        print(f"{p['pid']}\t{r['ct']}\t{r['tat']}\t{r['wt']}")


def round_robin(processes, quantum):
    print("\n--- Round Robin Scheduling ---")
    print(f"Time Quantum: {quantum}")

    # Sort by arrival time; stable ordering preserves input order for ties.
    jobs = sorted(processes, key=lambda p: p["at"])
    remaining = {p["pid"]: p["bt"] for p in jobs}
    results = {}
    ready = []
    gantt = []
    time = 0
    i = 0

    while i < len(jobs) or ready:
        if not ready and i < len(jobs) and time < jobs[i]["at"]:
            gantt.append(("IDLE", time, jobs[i]["at"]))
            time = jobs[i]["at"]

        # Add all processes that have arrived by current time.
        while i < len(jobs) and jobs[i]["at"] <= time:
            ready.append(jobs[i])
            i += 1

        if not ready:
            continue

        p = ready.pop(0)
        start = time
        run_time = min(quantum, remaining[p["pid"]])
        time += run_time
        remaining[p["pid"]] -= run_time

        gantt.append((p["pid"], start, time))

        # Add newly arrived processes before re-queuing the current process.
        while i < len(jobs) and jobs[i]["at"] <= time:
            ready.append(jobs[i])
            i += 1

        if remaining[p["pid"]] > 0:
            ready.append(p)
        else:
            ct = time
            results[p["pid"]] = {
                "ct": ct,
                "tat": ct - p["at"],
                "wt": ct - p["at"] - p["bt"]
            }

    print("Execution sequence:")
    for pid, start, end in gantt:
        print(f"| {pid} ({start}-{end}) ", end="")
    print("|")

    print("\nPID\tCT\tTAT\tWT")
    for p in processes:
        r = results[p["pid"]]
        print(f"{p['pid']}\t{r['ct']}\t{r['tat']}\t{r['wt']}")


try:
    processes = get_processes()
    quantum = int(input("\nEnter Round Robin time quantum: "))

    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    priority_scheduling(processes)
    round_robin(processes, quantum)

except ValueError as e:
    print("Input Error:", e)
