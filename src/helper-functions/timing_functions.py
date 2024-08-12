import psutil
import time
import threading


def monitor_time(stop_event, start_time):
    print("Monitoring started...")
    while not stop_event.is_set():
        current_time = time.time()
        elapsed_time = current_time - start_time  # Calculate elapsed time
        cpu_usage = psutil.cpu_percent(
            interval=1
        )  # interval=1 provides a 1-second delay for each loop iteration
        ram_usage = psutil.virtual_memory().available / (1024**2)  # Convert bytes to MB
        print(
            f"Elapsed Time: {elapsed_time:.2f}s, CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage:.2f} MB"
        )
    print("Function call completed, Monitoring stopped.")


def monitor_function(func, *args, **kwargs):
    start_time = time.time()
    stop_event = threading.Event()
    monitor_thread = threading.Thread(
        target=monitor_time, args=(stop_event, start_time)
    )  # Pass start_time to monitor_time

    monitor_thread.start()

    # Execute the provided function with its arguments
    result = func(*args, **kwargs)

    # Stop monitoring and wait for the monitoring thread to finish
    stop_event.set()
    monitor_thread.join()

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Function Execution Time: {execution_time:.4f} seconds")
    return result
