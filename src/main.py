import os
import time
import sys
import signal

import dsh.kafka.dsh_kafka as kafka
from loguru import logger


def main():
    producer_config = kafka.create_dsh_config()
    PRODUCE_TOPIC = os.environ["PRODUCE_TOPIC"]

    producer = kafka.create_producer(producer_config)

    signal.signal(signal.SIGTERM, handle_sigterm)

    run = True
    index = 0
    while run:
        kafka.produce_message(producer, f"hehehehe: {index}", PRODUCE_TOPIC)
        index += 1
        time.sleep(5)


def handle_sigterm(signum, frame):
    logger.warning("Receiving sigterm")
    sys.exit(1)


# Start
if __name__ == "__main__":
    main()
