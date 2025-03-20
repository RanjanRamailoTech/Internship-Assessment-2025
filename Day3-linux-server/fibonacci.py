import multiprocessing
import time

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def worker(n):
    print(f"Worker {multiprocessing.current_process().name} calculating Fibonacci({n})")
    result = fibonacci(n)
    print(f"Result of Fibonacci({n}) is {result}")

if __name__ == "__main__":
    numbers = [30, 32, 34, 36, 38, 40]
    
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        start_time = time.time()
        pool.map(worker, numbers)
        end_time = time.time()

    print(f"Total execution time: {end_time - start_time} seconds")
