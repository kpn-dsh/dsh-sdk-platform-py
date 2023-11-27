import queue
import threading
from typing import Literal
from loguru import logger
from icecream import ic

Test = Literal["A", "B", "C", "D"]


def worker(queue):
    while True:
        logger.info("Waiting for item")
        ic("hello")
        item = queue.get()
        match item:
            case "A":
                print("Received A")
            case "B":
                print("Received B")
            case "C":
                print("Received C")
            case _ as item:
                raise Exception(f"Unknown item: {item}")


# Create a queue
my_queue = queue.Queue()

# Create and start a worker thread
worker_thread = threading.Thread(target=worker, args=(my_queue,))
worker_thread.start()

# Enqueue some items with pattern matching
for _ in range(5):
    my_queue.put("A")
    my_queue.put("B")
    my_queue.put("C")
    # my_queue.put("hi there")

# Signal the worker to stop
my_queue.put(None)
worker_thread.join()
