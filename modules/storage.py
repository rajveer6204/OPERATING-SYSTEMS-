
"""
OS Resource Management Simulator
Disk Scheduling Algorithms
"""


def calculate_total_head_movement(sequence, initial_head):
    """Calculate total disk head movement."""
    total = 0
    current = initial_head

    for track in sequence:
        total += abs(track - current)
        current = track

    return total


def fcfs_disk(requests, initial_head):
    """First Come First Serve Disk Scheduling."""
    sequence = requests.copy()

    total = calculate_total_head_movement(sequence, initial_head)

    return sequence, total


def sstf_disk(requests, initial_head):
    """Shortest Seek Time First Disk Scheduling."""
    pending = requests.copy()
    sequence = []
    current = initial_head

    while pending:
        nearest = min(pending, key=lambda x: abs(x - current))

        sequence.append(nearest)
        pending.remove(nearest)
        current = nearest

    total = calculate_total_head_movement(sequence, initial_head)

    return sequence, total


def scan_disk(requests, initial_head, disk_size, direction="right"):
    """SCAN Disk Scheduling."""
    if direction not in ("left", "right"):
        raise ValueError("Direction must be 'left' or 'right'.")

    if not 0 <= initial_head < disk_size:
        raise ValueError("Initial head is outside the disk.")

    if any(not 0 <= track < disk_size for track in requests):
        raise ValueError("A request is outside the disk.")

    left = sorted([r for r in requests if r < initial_head])
    right = sorted([r for r in requests if r >= initial_head])

    sequence = []

    if direction == "right":
        sequence.extend(right)
        if left:
            sequence.append(disk_size - 1)
            sequence.extend(reversed(left))
    else:
        sequence.extend(reversed(left))
        if right:
            sequence.append(0)
            sequence.extend(right)

    # Remove unnecessary disk-end movement when no request exists
    # on the opposite side.
    total = calculate_total_head_movement(sequence, initial_head)

    return sequence, total


def cscan_disk(requests, initial_head, disk_size, direction="right"):
    """Circular SCAN Disk Scheduling."""
    if direction not in ("left", "right"):
        raise ValueError("Direction must be 'left' or 'right'.")

    if not 0 <= initial_head < disk_size:
        raise ValueError("Initial head is outside the disk.")

    if any(not 0 <= track < disk_size for track in requests):
        raise ValueError("A request is outside the disk.")

    left = sorted([r for r in requests if r < initial_head])
    right = sorted([r for r in requests if r >= initial_head])

    sequence = []

    if direction == "right":
        sequence.extend(right)
        if left:
            sequence.append(disk_size - 1)
            sequence.append(0)
            sequence.extend(left)
    else:
        sequence.extend(reversed(left))
        if right:
            sequence.append(0)
            sequence.append(disk_size - 1)
            sequence.extend(reversed(right))

    total = calculate_total_head_movement(sequence, initial_head)

    return sequence, total


def validate_input(requests, initial_head, disk_size):
    """Validate disk scheduling input."""
    if not requests:
        raise ValueError("Disk request list cannot be empty.")

    if disk_size <= 0:
        raise ValueError("Disk size must be positive.")

    if not 0 <= initial_head < disk_size:
        raise ValueError("Initial head is outside the disk.")

    if any(not isinstance(r, int) or not 0 <= r < disk_size
           for r in requests):
        raise ValueError("All requests must be valid disk track numbers.")


def display_result(name, sequence, total):
    """Display disk scheduling result."""
    print("\n===================================")
    print(name)
    print("===================================")

    print("Head Movement Sequence:", end=" ")
    print(initial_head, end="")

    for track in sequence:
        print(" ->", track, end="")

    print("\nTotal Head Movement:", total, "tracks")


if __name__ == "__main__":

    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    initial_head = 53
    disk_size = 200

    validate_input(requests, initial_head, disk_size)

    print("OS RESOURCE MANAGEMENT SIMULATOR")
    print("DISK SCHEDULING MODULE")

    print("\nDisk Requests:", requests)
    print("Initial Head Position:", initial_head)
    print("Disk Size:", disk_size)

    sequence, total = fcfs_disk(requests, initial_head)
    display_result("FCFS DISK SCHEDULING", sequence, total)

    sequence, total = sstf_disk(requests, initial_head)
    display_result("SSTF DISK SCHEDULING", sequence, total)

    sequence, total = scan_disk(
        requests, initial_head, disk_size, "right"
    )
    display_result("SCAN DISK SCHEDULING", sequence, total)

    sequence, total = cscan_disk(
        requests, initial_head, disk_size, "right"
    )
    display_result("C-SCAN DISK SCHEDULING", sequence, total)
