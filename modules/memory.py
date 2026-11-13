
# ==========================================
# OS RESOURCE MANAGEMENT SIMULATOR
# MODULE: MEMORY MANAGEMENT
# ==========================================


# Common function for memory allocation

def allocate_memory(processes, blocks, method):

    if not processes:
        raise ValueError("At least one process is required")

    if not blocks:
        raise ValueError("At least one memory block is required")

    if any(p <= 0 for p in processes):
        raise ValueError("Process sizes must be positive")

    if any(b <= 0 for b in blocks):
        raise ValueError("Memory blocks must be positive")

    remaining_blocks = blocks.copy()

    results = []

    for i, process_size in enumerate(processes):

        selected_block = -1

        if method == "First Fit":

            for j in range(len(remaining_blocks)):

                if remaining_blocks[j] >= process_size:
                    selected_block = j
                    break

        elif method == "Best Fit":

            suitable = [
                j for j in range(len(remaining_blocks))
                if remaining_blocks[j] >= process_size
            ]

            if suitable:
                selected_block = min(
                    suitable,
                    key=lambda j: remaining_blocks[j]
                )

        elif method == "Worst Fit":

            suitable = [
                j for j in range(len(remaining_blocks))
                if remaining_blocks[j] >= process_size
            ]

            if suitable:
                selected_block = max(
                    suitable,
                    key=lambda j: remaining_blocks[j]
                )

        else:
            raise ValueError("Invalid allocation method")

        if selected_block != -1:

            remaining_blocks[selected_block] -= process_size

            results.append({
                "process": f"P{i + 1}",
                "size": process_size,
                "block": selected_block + 1,
                "remaining": remaining_blocks[selected_block],
                "status": "Allocated"
            })

        else:

            results.append({
                "process": f"P{i + 1}",
                "size": process_size,
                "block": "Not Available",
                "remaining": "-",
                "status": "Not Allocated"
            })

    return results


# Display allocation results

def display_memory_results(method, results):

    print("\n===================================")
    print(method.upper(), "MEMORY ALLOCATION")
    print("===================================")

    print("\nProcess\tSize\tBlock\t\tStatus")

    for item in results:

        print(
            f"{item['process']}\t"
            f"{item['size']}\t"
            f"{item['block']}\t\t"
            f"{item['status']}"
        )


# Main program

if __name__ == "__main__":

    memory_blocks = [100, 500, 200, 300, 600]

    process_sizes = [212, 417, 112, 426]

    print("\nOS RESOURCE MANAGEMENT SIMULATOR")
    print("MEMORY MANAGEMENT MODULE")

    print("\nMemory Blocks:", memory_blocks)
    print("Process Sizes:", process_sizes)

    methods = ["First Fit", "Best Fit", "Worst Fit"]

    for method in methods:

        result = allocate_memory(
            process_sizes,
            memory_blocks,
            method  
        )

        display_memory_results(method, result)
