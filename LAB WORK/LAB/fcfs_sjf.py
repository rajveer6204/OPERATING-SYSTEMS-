
def get_processes():
    processes = []
    seen_ids = set()

    try:
        n = int(input("Enter number of processes: "))
        if n <= 0:
            raise ValueError("Number of processes must be positive.")

        for i in range(n):
            print(f"\nProcess {i + 1}")
            pid = input("Process ID: ").strip()

            if not pid or pid in seen_ids:
                raise ValueError("Process ID must be non-empty and unique.")
            seen_ids.add(pid)

            arrival = int(input("Arrival Time: "))
            burst = int(input("Burst Time: "))

            if arrival < 0:
                raise ValueError("Arrival Time cannot be negative.")
            if burst <= 0:
                raise ValueError("Burst Time must be positive.")

            processes.append({
                "pid": pid,
                "arrival": arrival,
                "burst": burst
            })

    except ValueError as e:
        print("Invalid input:", e)
        return None

    return processes


def schedule(processes, algorithm):
    # Copy data so the original dataset stays unchanged.
    remaining = [p.copy() for p in processes]
    result = []
    time = 0

    while remaining:
        available = [
            p for p in remaining
            if p["arrival"] <= time
        ]

        if not available:
            next_arrival = min(p["arrival"] for p in remaining)
            result.append({
                "pid": "IDLE",
                "start": time,
                "end": next_arrival
            })
            time = next_arrival
            continue

        if algorithm == "FCFS":
            # Earliest arrival; input order breaks arrival ties.
            chosen = min(
                available,
                key=lambda p: (p["arrival"],
                               processes.index(next(
                                   original for original in processes
                                   if original["pid"] == p["pid"]
                               )))
            )
        else:
            # Shortest burst among arrived processes.
            # Arrival time, then input order, breaks ties.
            chosen = min(
                available,
                key=lambda p: (
                    p["burst"],
                    p["arrival"],
                    next(i for i, original in enumerate(processes)
                         if original["pid"] == p["pid"])
                )
            )

        start = time
        end = time + chosen["burst"]

        result.append({
            "pid": chosen["pid"],
            "start": start,
            "end": end
        })

        time = end
        remaining.remove(chosen)

    return result


def display_schedule(name, result):
    print(f"\n--- {name} Scheduling ---")
    print("Execution sequence:")
    print(" -> ".join(
        f'{item["pid"]} [{item["start"]}-{item["end"]}]'
        for item in result
    ))

    print("\nProcess\tStart\tEnd")
    for item in result:
        print(f'{item["pid"]}\t{item["start"]}\t{item["end"]}')


def main():
    processes = get_processes()

    if processes is None:
        return

    print("\nOriginal process dataset:")
    print("PID\tArrival\tBurst")
    for p in processes:
        print(f'{p["pid"]}\t{p["arrival"]}\t{p["burst"]}')

    fcfs_result = schedule(processes, "FCFS")
    sjf_result = schedule(processes, "SJF")

    display_schedule("FCFS", fcfs_result)
    display_schedule("Non-Preemptive SJF", sjf_result)

    print("\nOriginal dataset preserved:", processes)


if __name__ == "__main__":
    main()
