import time

while True:
    with open("/tmp/hello_world.log", "a") as log_file:
        log_file.write("Hello from systemd! The time is: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    time.sleep(10)
