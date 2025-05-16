import os
import time
import sys
import signal

import dsh.kafka.dsh_kafka as kafka


def main():
    producer_config = kafka.create_dsh_config()
    PRODUCE_TOPIC = os.environ["PRODUCE_TOPIC"]

    producer = kafka.create_producer(producer_config)

    count = 0
    while True:
        value = f"message-{count}"
        try:
            producer.produce(PRODUCE_TOPIC, value)
            producer.flush()
            print(f"Produced: {value}")
        except Exception as e:
            print(f"Failed to produce message: {e}")

        count += 1
        time.sleep(5)

    signal.signal(signal.SIGTERM, handle_sigterm)


def handle_sigterm(signum, frame):
    print("Receiving sigterm")
    sys.exit(1)


# Start
if __name__ == "__main__":
    main()
