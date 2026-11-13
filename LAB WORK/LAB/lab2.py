import threading
import _thread
import time
import os
import math

def perform_task_chunk(task_id, start_range, end_range, progress_callback=None):
    thread_name = threading.current_thread().name
    thread_ident = threading.current_thread().ident
    native_id = getattr(threading, "get_native_id", lambda: "N/A")()
    
    total_items = end_range - start_range
    step_checkpoint = max(1, total_items // 4)
    processed_count = 0
    accumulator = 0
    
    for number in range(start_range, end_range):
        accumulator += (number * number) % 10000007
        time.sleep(0.00002)
        processed_count += 1
        
        if progress_callback and (processed_count % step_checkpoint == 0 or processed_count == total_items):
            pct = int((processed_count / total_items) * 100)
            progress_callback(task_id, thread_name, native_id, thread_ident, pct, processed_count, total_items)
            
    return accumulator

def run_single_threaded(workload_chunks):
    print("=" * 80)
    print("PHASE 1: SINGLE-THREADED BASELINE WORKLOAD EXECUTION")
    print("=" * 80)
    print(f"Total workload divided into {len(workload_chunks)} sequential chunks.")
    print("Executing all tasks on the main thread sequentially...\n")
    
    def single_thread_progress(task_id, t_name, nat_id, ident, pct, done, total):
        print(f" [Single-Threaded] Task-{task_id} | Thread: {t_name} | Progress: {pct:3d}% ({done}/{total} units)")
        
    start_time = time.perf_counter()
    results = []
    
    for task_id, (start_idx, end_idx) in enumerate(workload_chunks, start=1):
        print(f"--> Starting Task-{task_id} range: [{start_idx}, {end_idx})")
        res = perform_task_chunk(task_id, start_idx, end_idx, progress_callback=single_thread_progress)
        results.append(res)
        print(f"--- Finished Task-{task_id} with checksum: {res}\n")
        
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Single-Threaded Total Execution Time: {duration:.4f} seconds")
    return duration, results

def run_multithreaded(workload_chunks):
    print("\n" + "=" * 80)
    print("PHASE 2: MULTITHREADED WORKLOAD EXECUTION (THREAD CREATION & JOIN)")
    print("=" * 80)
    num_threads = len(workload_chunks)
    print(f"Creating {num_threads} worker threads using Python 'threading' module.")
    print("Each thread executes an independent partition concurrently.\n")
    
    thread_results = [None] * num_threads
    thread_lock = threading.Lock()
    
    def worker_wrapper(task_index, start_idx, end_idx):
        def thread_progress(task_id, t_name, nat_id, ident, pct, done, total):
            with thread_lock:
                print(f" [Worker Thread] Task-{task_id:02d} | Name: {t_name:10s} | Native TID: {str(nat_id):8s} | Ident: {ident} | Progress: {pct:3d}%")
        
        result = perform_task_chunk(task_index + 1, start_idx, end_idx, progress_callback=thread_progress)
        thread_results[task_index] = result
        
    threads = []
    start_time = time.perf_counter()
    
    for i, (start_idx, end_idx) in enumerate(workload_chunks):
        t = threading.Thread(
            target=worker_wrapper,
            args=(i, start_idx, end_idx),
            name=f"Worker-{i+1}"
        )
        threads.append(t)
        
    print("Starting all worker threads...")
    for t in threads:
        t.start()
        print(f" * Dispatched {t.name} (Thread Alive: {t.is_alive()}, Ident: {t.ident})")
        
    print("\nDisplaying real-time concurrent thread execution progress:")
    print("-" * 80)
    
    for t in threads:
        t.join()
        with thread_lock:
            print(f" * Joined {t.name} (Execution complete, Alive: {t.is_alive()})")
            
    end_time = time.perf_counter()
    duration = end_time - start_time
    print("-" * 80)
    print(f"Multithreaded Total Execution Time: {duration:.4f} seconds")
    return duration, thread_results

def print_workload_comparison(single_time, multi_time, num_tasks):
    print("\n" + "=" * 80)
    print("PHASE 3: WORKLOAD PERFORMANCE COMPARISON")
    print("=" * 80)
    speedup = single_time / multi_time if multi_time > 0 else 0.0
    time_saved = single_time - multi_time
    pct_reduction = ((single_time - multi_time) / single_time) * 100 if single_time > 0 else 0.0
    
    print(f"Total Independent Workload Tasks : {num_tasks}")
    print(f"Single-Threaded Execution Time   : {single_time:.4f} seconds")
    print(f"Multithreaded Execution Time     : {multi_time:.4f} seconds")
    print(f"Absolute Time Saved              : {time_saved:.4f} seconds")
    print(f"Speedup Factor                   : {speedup:.2f}x")
    print(f"Execution Time Reduction         : {pct_reduction:.2f}%\n")
    
    if speedup > 1.0:
        print("Comparison Verdict: Multithreading demonstrated significant latency reduction by")
        print("overlapping task latency and achieving concurrent execution across available CPU resources.")
    else:
        print("Comparison Verdict: Both versions finished with comparable times due to system load.")

def discuss_threading_models():
    print("\n" + "=" * 80)
    print("THEORETICAL ANALYSIS PART 1: THREAD TYPES & MULTITHREADING MODELS")
    print("=" * 80)
    
    print("\n1. USER-LEVEL THREADS (ULT) vs KERNEL-LEVEL THREADS (KLT):")
    print("-" * 75)
    print("a. User-Level Threads (ULT):")
    print("   - Managed entirely by runtime user-space thread libraries (e.g., POSIX pthreads without kernel bind).")
    print("   - Thread switching does not require kernel mode transitions, making switching fast and lightweight.")
    print("   - Drawback: The OS kernel sees only one process. If one user thread executes a blocking system call,")
    print("     the entire process (and all other user threads within it) is blocked by the kernel.")
    print("   - Cannot achieve true multicore parallelism because the OS schedules the process onto a single CPU core.")
    
    print("\nb. Kernel-Level Threads (KLT):")
    print("   - Managed, scheduled, and recognized directly by the operating system kernel.")
    print("   - The kernel maintains context information for both processes and individual threads.")
    print("   - Advantage: If one thread blocks on I/O, the kernel can freely schedule another thread of the same process.")
    print("   - Advantage: Kernel can distribute threads of the same process across multiple physical CPU cores.")
    print("   - Cost: Thread creation, termination, and context switching incur kernel trap and mode switch overhead.")

    print("\n2. COMMON MULTITHREADING MODELS:")
    print("-" * 75)
    print("a. Many-to-One Model:")
    print("   - Maps many user-level threads to a single kernel thread.")
    print("   - Thread management happens in user space, so it is highly efficient.")
    print("   - Major limitation: If a thread performs a blocking call, the entire process halts.")
    print("   - Multiple threads cannot run in parallel on multicore systems.")
    
    print("b. One-to-One Model (Standard in Windows and Linux):")
    print("   - Maps each user-level thread directly to a dedicated kernel thread.")
    print("   - Provides superior concurrency: blocking calls in one thread do not hinder others.")
    print("   - Fully exploits multiprocessor/multicore hardware architectures.")
    print("   - Primary drawback: Creating too many threads can strain kernel resources and degrade performance.")
    
    print("c. Many-to-Many Model:")
    print("   - Multiplexes many user-level threads onto an equal or smaller number of kernel threads.")
    print("   - Developers can create as many user threads as required without unbounded kernel thread allocation.")
    print("   - The kernel schedules the kernel threads on physical processors, balancing efficiency and concurrency.")
    print("   - Variations include the Two-Level Model, which allows certain critical user threads to bind 1:1.")

def discuss_concurrency_and_benefits():
    print("\n" + "=" * 80)
    print("THEORETICAL ANALYSIS PART 2: BENEFITS, CHALLENGES & SYSTEM OVERHEAD")
    print("=" * 80)
    
    print("\n1. CORE BENEFITS OF MULTITHREADING:")
    print("-" * 75)
    print("a. Responsiveness:")
    print("   - An interactive application can remain fully responsive to user input while background threads")
    print("     perform computationally heavy or long-running I/O operations (e.g., UI remains fluid during downloads).")
    
    print("b. Resource Sharing:")
    print("   - Threads of the same process inherently share memory address space, global variables, and open file descriptors.")
    print("   - Unlike processes that require costly IPC (pipes, shared memory segments, message queues), threads share data")
    print("     naturally without inter-process memory duplication.")
    
    print("c. Economy and Low Overhead:")
    print("   - Allocating memory and resources for process creation is significantly more expensive than thread creation.")
    print("   - Thread context switching is faster because memory management structures (page tables) remain unchanged.")

    print("\n2. CONCURRENCY vs PARALLELISM:")
    print("-" * 75)
    print("a. Concurrency:")
    print("   - Managing and executing multiple tasks by interleaving their execution over time on a single or multiple cores.")
    print("   - Concurrency is about application structure and handling multiple events simultaneously.")
    
    print("b. Parallelism:")
    print("   - Simultaneously executing multiple computational tasks at the exact same physical instant on separate CPU cores.")
    print("   - Requires multicore or multiprocessor hardware architecture.")

    print("\n3. MULTITHREADING HAZARDS AND CHALLENGES:")
    print("-" * 75)
    print("a. Race Conditions:")
    print("   - Occurs when multiple threads access and mutate shared data concurrently without proper synchronization.")
    print("   - The final outcome depends on the non-deterministic order of thread execution and scheduling.")
    print("   - Prevention: Employ synchronization primitives such as Mutexes, Locks, and Semaphores to enforce mutual exclusion.")
    
    print("b. Deadlocks:")
    print("   - Occurs when two or more threads are permanently blocked, each waiting for a resource held by the other.")
    print("   - Characterized by Coffman conditions: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.")
    print("   - Mitigation: Strict resource ordering, timeout mechanisms, and deadlock avoidance algorithms.")
    
    print("c. Threading Overhead:")
    print("   - Creating and destroying threads consumes CPU cycles and system memory (thread stacks, TCB structures).")
    print("   - Frequent context switching introduces CPU cache misses and OS scheduler overhead.")
    print("   - In Python (CPython), CPU-bound threads are serialized by the Global Interpreter Lock (GIL), while I/O-bound")
    print("     threads achieve high concurrency by releasing the GIL during blocking operations.")

def main():
    print("=" * 80)
    print("OPERATING SYSTEMS LAB: THREAD CREATION, MODELS AND BENEFITS")
    print("=" * 80)
    print(f"Operating System Platform : {os.name.upper()} (Process ID: {os.getpid()})")
    print(f"Available CPU Cores       : {os.cpu_count()}")
    print(f"Main Thread Identifier    : {threading.current_thread().name} (Ident: {threading.current_thread().ident})\n")
    
    total_items = 2000
    num_tasks = 4
    chunk_size = total_items // num_tasks
    workload_chunks = []
    
    for i in range(num_tasks):
        start_idx = i * chunk_size
        end_idx = total_items if i == num_tasks - 1 else (i + 1) * chunk_size
        workload_chunks.append((start_idx, end_idx))
        
    single_time, single_results = run_single_threaded(workload_chunks)
    multi_time, multi_results = run_multithreaded(workload_chunks)
    
    print_workload_comparison(single_time, multi_time, num_tasks)
    discuss_threading_models()
    discuss_concurrency_and_benefits()
    
    print("\n" + "=" * 80)
    print("EXECUTION AND CONCEPTUAL DISCUSSION COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    main()