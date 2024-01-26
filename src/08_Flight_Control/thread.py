import threading
import time

class MyThread(threading.Thread):
    def __init__(self, thread_id, name, delay):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.delay = delay

    def run(self):
        print(f"Starting {self.name}")
        self.print_time()
        print(f"Exiting {self.name}")

    def print_time(self):
        counter = 5
        while counter:
            time.sleep(self.delay)
            print(f"{self.name}: {time.ctime(time.time())}")
            counter -= 1

# Create instances of MyThread
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 5)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Main thread exiting.")