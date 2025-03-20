import multiprocessing
import time

def background_task():
    while True:
        print(f"Daemon process running in the background (PID: {multiprocessing.current_process().pid})")
        time.sleep(2)

def main_task():
    print("Main process started.")
    for i in range(5):
        print(f"Main task running... {i + 1}")
        time.sleep(1)
    print("Main process finished.")

if __name__ == "__main__":
    daemon_process = multiprocessing.Process(target=background_task)
    daemon_process.daemon = True
    
    daemon_process.start()
    main_task()
    
    print("Main process has finished. Daemon process will be killed.")
