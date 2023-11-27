import packet
import queue
import threading

# packet.


def main():
    # Create a queue
    my_queue = queue.Queue()

    # Create and start a worker thread
    worker_thread = threading.Thread(target=worker, args=(my_queue,))
    worker_thread.start()

    # Enqueue some items with pattern matching
    for _ in range(5):
        my_queue.put(packet.Header(protocol="HTTP", size=10))
        my_queue.put(packet.Payload(data="Hello"))
        my_queue.put(packet.Trailer(data="World", checksum=42))

    # Signal the worker to stop
    my_queue.put(None)
    worker_thread.join()


def worker(queue: queue.Queue):
    while True:
        item = queue.get()
        if item is None:
            break
        packet.match(item)


if __name__ == "__main__":
    main()
