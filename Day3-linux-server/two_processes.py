import multiprocessing
import time

def first_task():
    print("First task started.")
    for i in range(5):
        print(f"First task running... {i + 1}")
        time.sleep(1)
    print("First task finished.")

def second_task():
    print("Second task started and running indefinitely.")
    while True:
        print("Second task is running...")
        time.sleep(2)

if __name__ == "__main__":
    process1 = multiprocessing.Process(target=first_task)
    process1.start()

    process2 = multiprocessing.Process(target=second_task)
    process2.start()

    process1.join()

    print("First task finished. Second task continues running...")
